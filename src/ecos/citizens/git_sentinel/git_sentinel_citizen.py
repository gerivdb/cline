"""
GitSentinel Citizen - Interface CLINE vers ECOS-CLI
Redirection vers l'implémentation réelle dans ECOS-CLI.
"""

import sys
import os

# Chemin vers ECOS-CLI
ecos_cli_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'ECOS-CLI', 'src')
if ecos_cli_path not in sys.path:
    sys.path.insert(0, ecos_cli_path)

try:
    # Import et réexport depuis ECOS-CLI
    from ecos.citizens.git_sentinel.git_sentinel_citizen import GitSentinelCitizen as _GitSentinelCitizen
    from ecos.citizens.git_sentinel.sync_orchestrator import SyncOrchestrator as _SyncOrchestrator
    from ecos.citizens.git_sentinel.conflict_resolver import ConflictResolver as _ConflictResolver
    from ecos.citizens.git_sentinel.commit_validator import CommitValidator as _CommitValidator
    from ecos.citizens.git_sentinel.branch_manager import BranchManager as _BranchManager
    from ecos.citizens.git_sentinel.security_auditor import SecurityAuditor as _SecurityAuditor
    from ecos.citizens.git_sentinel.performance_optimizer import PerformanceOptimizer as _PerformanceOptimizer
    from ecos.citizens.git_sentinel.predictive_analyzer import PredictiveAnalyzer as _PredictiveAnalyzer
    from ecos.citizens.git_sentinel.federation_manager import FederationManager as _FederationManager

    # Réexport avec les mêmes noms
    GitSentinelCitizen = _GitSentinelCitizen
    SyncOrchestrator = _SyncOrchestrator
    ConflictResolver = _ConflictResolver
    CommitValidator = _CommitValidator
    BranchManager = _BranchManager
    SecurityAuditor = _SecurityAuditor
    PerformanceOptimizer = _PerformanceOptimizer
    PredictiveAnalyzer = _PredictiveAnalyzer
    FederationManager = _FederationManager

except ImportError as e:
    # Fallback si ECOS-CLI n'est pas disponible
    print(f"⚠️  GitSentinel non disponible depuis CLINE: {e}")
    print("💡 Assurez-vous qu'ECOS-CLI est installé et accessible")

    # Classes stub
    class _StubClass:
        def __init__(self, *args, **kwargs):
            raise ImportError("GitSentinel requires ECOS-CLI to be available. Please ensure ECOS-CLI is properly installed.")

    GitSentinelCitizen = _StubClass
    SyncOrchestrator = _StubClass
    ConflictResolver = _StubClass
    CommitValidator = _StubClass
    BranchManager = _StubClass
    SecurityAuditor = _StubClass
    PerformanceOptimizer = _StubClass
    PredictiveAnalyzer = _StubClass
    FederationManager = _StubClass
