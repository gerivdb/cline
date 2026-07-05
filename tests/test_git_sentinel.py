"""
Test rapide de GitSentinel - Pool de Citoyens Git SOTA

Note: GitSentinel est maintenant développé dans ECOS-CLI.
Ce fichier est maintenu pour compatibilité mais les vrais tests sont dans ../ECOS-CLI/
"""

import asyncio
import sys
import os

async def test_git_sentinel():
    """Test du système GitSentinel."""
    print("Test de GitSentinel - Gestion Git SOTA")
    print("GitSentinel est maintenant dans ECOS-CLI")
    print("Executez ce test depuis: ../ECOS-CLI/")
    print("Commande: python test_git_sentinel.py")

    try:
        # Essayer d'importer depuis ECOS-CLI
        ecos_cli_path = os.path.join(os.path.dirname(__file__), '..', 'ECOS-CLI', 'src')
        if os.path.exists(ecos_cli_path):
            sys.path.insert(0, ecos_cli_path)
            from ecos.citizens.git_sentinel.git_sentinel_citizen import GitSentinelCitizen

            # Créer GitSentinel
            git_sentinel = GitSentinelCitizen("test_git_sentinel")
            print("GitSentinel cree depuis ECOS-CLI")

            # Tester les opérations Git basiques
            status = await git_sentinel.get_status_report()
            print(f"Status rapporte: {status.get('overall_health', 'unknown')}")

            return True
        else:
            print("Repertoire ECOS-CLI non trouve")
            return False

    except Exception as e:
        print(f"Erreur test GitSentinel: {e}")
        print("Assurez-vous d'executer depuis ECOS-CLI: cd ../ECOS-CLI && python test_git_sentinel.py")
        return False

async def main():
    """Test principal."""
    print("Tests GitSentinel")
    print("=" * 50)

    success = await test_git_sentinel()

    print("=" * 50)
    if success:
        print("GitSentinel operationnel - Gestion Git SOTA activee!")
    else:
        print("Tests echoues - Verifiez que vous etes dans ECOS-CLI")

if __name__ == "__main__":
    asyncio.run(main())
