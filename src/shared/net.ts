/**
 * # Network Support for Cline
 *
 * ## Development Guidelines
 *
 * **Do** use `import { fetch } from '@/shared/net'` instead of global `fetch`.
 *
 * Global `fetch` will appear to work in VSCode, but proxy support will be
 * broken in JetBrains or CLI.
 *
 * If you use Axios, **do** call `getAxiosSettings()` and spread into
 * your Axios configuration:
 *
 * ```typescript
 * import { getAxiosSettings } from '@/shared/net'
 * await axios.get(url, {
 *   headers: { 'X-FOO': 'BAR' },
 *   ...getAxiosSettings()
 * })
 * ```
 *
 * **Do** remember to pass our `fetch` into your API clients:
 *
 * ```typescript
 * import OpenAI from "openai"
 * import { fetch } from "@/shared/net"
 * this.client = new OpenAI({
 *   apiKey: '...',
 *   fetch, // Use configured fetch with proxy support
 * })
 * ```
 *
 * If you neglect this step, inference won't work in JetBrains and CLI
 * through proxies.
 *
 * ## Proxy Support
 *
 * Cline uses platform-specific fetch implementations to handle proxy
 * configuration:
 * - **VSCode**: Uses global fetch (VSCode provides proxy configuration)
 * - **JetBrains, CLI**: Uses undici fetch with explicit ProxyAgent
 *
 * Proxy configuration via standard environment variables:
 * - `http_proxy` / `HTTP_PROXY` - Proxy for HTTP requests
 * - `https_proxy` / `HTTPS_PROXY` - Proxy for HTTPS requests
 * - `no_proxy` / `NO_PROXY` - Comma-separated list of hosts to bypass proxy
 *
 * Note, `http_proxy` etc. MUST specify the protocol to use for the proxy,
 * for example, `https_proxy=http://proxy.corp.example:3128`. Simply specifying
 * the proxy hostname will result in errors.
 *
 * ## Certificate Trust
 *
 * **Standalone Mode (JetBrains, CLI)**: Automatically loads trusted certs
 * from the operating system using the `system-ca` package:
 * - Windows: Trusted Root Certification Authorities store
 * - macOS: System and user keychains
 * - Linux: Standard certificate directories (/etc/ssl/certs, etc.)
 *
 * **VSCode**: Transparently pulls trusted certificates from the operating
 * system and configures node trust.
 *
 * ## Initialization
 *
 * For standalone mode, call `initializeNetworkConfig()` early in your startup
 * sequence, before making any network requests:
 *
 * ```typescript
 * import { initializeNetworkConfig } from '@/shared/net'
 * await initializeNetworkConfig()
 * ```
 *
 * ## Limitations in JetBrains & CLI
 *
 * - Proxy settings are static at startup--restart required for changes
 * - SOCKS proxies, PAC files not supported
 * - Proxy authentication via env vars only
 *
 * These are not fundamental limitations, they just need integration work.
 *
 * ## Troubleshooting
 *
 * 1. Verify proxy env vars: `echo $http_proxy $https_proxy`
 * 2. Check certificates: `echo $NODE_EXTRA_CA_CERTS` (should point to PEM file)
 * 3. View logs: Check ~/.cline/cline-core-service.log for network-related
 *    failures and certificate loading status.
 * 4. Test connection: Use `curl -x host:port` etc. to isolate proxy
 *    configuration versus client issues.
 *
 * @example
 * ```typescript
 * // Good - uses configured fetch
 * import { fetch } from '@/shared/net'
 * const response = await fetch(url)
 *
 * // Good - configures axios to use configured fetch
 * import { getAxiosSettings } from '@/shared/net'
 * await axios.get(url, { ...getAxiosSettings() })
 * ```
 */

import * as fs from "fs/promises"
import { systemCertsAsync } from "system-ca"
import { EnvHttpProxyAgent, setGlobalDispatcher, fetch as undiciFetch } from "undici"

// Certificate cache for standalone mode
let cachedCertificates: string[] | undefined

let mockFetch: typeof globalThis.fetch | undefined

/**
 * Initialize network configuration for standalone mode.
 * This function:
 * 1. Loads OS certificates using system-ca
 * 2. Includes Node.js built-in certificates
 * 3. Optionally merges certificates from NODE_EXTRA_CA_CERTS
 * 4. Configures undici agent with certificates and proxy support
 *
 * Should be called once at startup before any network requests.
 * Safe to call in VSCode mode - will be a no-op.
 *
 * @returns Promise that resolves when network configuration is complete
 */
export async function initializeNetworkConfig(log: (...args: unknown[]) => void): Promise<void> {
	// Only initialize in standalone mode
	if (!process.env.IS_STANDALONE) {
		log("intializeNetworkConfig is not running standalone and will not load certificate authorities")
		return
	}

	// Load certificates
	const errors: string[] = []
	let certificates: string[] = []

	try {
		// Load OS certificates + Node.js built-ins
		// system-ca returns an array of PEM-formatted certificate strings
		certificates = await systemCertsAsync({
			includeNodeCertificates: true,
		})

		// Optional: Also load from NODE_EXTRA_CA_CERTS if set
		// Note: Node.js will automatically use this env var, but we include
		// it here for consistency and to ensure all certs are in one place
		if (process.env.NODE_EXTRA_CA_CERTS) {
			try {
				const extraCerts = await fs.readFile(process.env.NODE_EXTRA_CA_CERTS, "utf-8")
				certificates.push(extraCerts)
			} catch (err) {
				errors.push(`Failed to load NODE_EXTRA_CA_CERTS: ${err}`)
			}
		}

		cachedCertificates = certificates
		log(`initializeNetworkConfig: loaded ${certificates.length} system certificates`)
		if (errors.length > 0) {
			log("initializeNetworkConfig: certificate loading warnings", errors.join("\n"))
		}
	} catch (err) {
		// Non-fatal: fall back to Node.js built-ins
		log("initializeNetworkConfig: failed to load system certificates:", err)
		log("initializeNetworkConfig: falling back to Node.js built-in certificates")
		cachedCertificates = undefined
	}

	// Now reconfigure the agent with certificates
	const agentOptions: any = {}
	if (cachedCertificates?.length) {
		agentOptions.connect = {
			ca: cachedCertificates,
		}
	}

	const agent = new EnvHttpProxyAgent(agentOptions)
	setGlobalDispatcher(agent)
}

/**
 * fetch that respects proxy settings and certificate trust. Use this instead of
 * global fetch to ensure proper proxy and certificate configuration.
 *
 * @example
 * ```typescript
 * import { fetch } from '@/shared/net'
 * const response = await fetch('https://api.example.com')
 * ```
 */
export const fetch: typeof globalThis.fetch = (() => {
	// Note: Don't use Logger here; it may not be initialized.

	let baseFetch: typeof globalThis.fetch = globalThis.fetch
	// Note: See esbuild.mjs, process.env.IS_STANDALONE is statically rewritten
	// 'true' in the JetBrains/CLI build.
	if (process.env.IS_STANDALONE) {
		// Create initial agent without certificates (will be reconfigured in initializeNetworkConfig)
		const agent = new EnvHttpProxyAgent({})
		setGlobalDispatcher(agent)
		baseFetch = undiciFetch as any as typeof globalThis.fetch
	}

	return (input: string | URL | Request, init?: RequestInit): Promise<Response> => (mockFetch || baseFetch)(input, init)
})()

/**
 * Mocks `fetch` for testing and calls `callback`. Then restores `fetch`. If the
 * specified callback returns a Promise, the fetch is restored when that Promise
 * is settled.
 * @param theFetch the replacement function to call to implement `fetch`.
 * @param callback `fetch` will be mocked for the duration of `callback()`.
 * @returns the result of `callback()`.
 */
export function mockFetchForTesting<T>(theFetch: typeof globalThis.fetch, callback: () => T): T {
	const originalMockFetch = mockFetch
	mockFetch = theFetch
	let willResetSync = true
	try {
		const result = callback()
		if (result instanceof Promise) {
			willResetSync = false
			return result.finally(() => {
				mockFetch = originalMockFetch
			}) as typeof result
		} else {
			return result
		}
	} finally {
		if (willResetSync) {
			mockFetch = originalMockFetch
		}
	}
}

/**
 * Returns axios configuration for fetch adapter mode with our configured fetch.
 * This ensures axios uses our platform-specific fetch implementation with
 * proper proxy configuration.
 *
 * @returns Configuration object with fetch adapter and configured fetch
 *
 * @example
 * ```typescript
 * const response = await axios.get(url, {
 *   headers: { Authorization: 'Bearer token' },
 *   timeout: 5000,
 *   ...getAxiosSettings()
 * })
 * ```
 */
export function getAxiosSettings(): { adapter?: any; fetch?: typeof globalThis.fetch } {
	return {
		adapter: "fetch" as any,
		fetch, // Use our configured fetch
	}
}
