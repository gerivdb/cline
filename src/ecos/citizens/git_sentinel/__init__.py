"""
GitSentinel - Pool de Citoyens pour Gestion Git SOTA
Interface CLINE vers ECOS-CLI GitSentinel.
"""

import sys
import os
from typing import TYPE_CHECKING

# Chemin vers ECOS-CLI
ecos_cli_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'ECOS-CLI', 'src')
if ecos_cli_path not in sys.path:
    sys.path.insert(0, ecos_cli_path)

try:
    # Import depuis ECOS-CLI
    from ecos.citizens.git_sentinel.git_sentinel_citizen import GitSentinelCitizen
    from ecos.citizens.git_sentinel.sync_orchestrator import SyncOrchestrator
    from ecos.citizens.git_sentinel.conflict_resolver import ConflictResolver
    from ecos.citizens.git_sentinel.commit_validator import CommitValidator
    from ecos.citizens.git_sentinel.branch_manager import BranchManager
    from ecos.citizens.git_sentinel.security_auditor import SecurityAuditor
    from ecos.citizens.git_sentinel.performance_optimizer import PerformanceOptimizer
    from ecos.citizens.git_sentinel.predictive_analyzer import PredictiveAnalyzer
    from ecos.citizens.git_sentinel.federation_manager import FederationManager

    __all__ = [
        'GitSentinelCitizen',
        'SyncOrchestrator',
        'ConflictResolver',
        'CommitValidator',
        'BranchManager',
        'SecurityAuditor',
        'PerformanceOptimizer',
        'PredictiveAnalyzer',
        'FederationManager'
    ]

except ImportError as e:
    # Fallback si ECOS-CLI n'est pas disponible
    print(f"⚠️  GitSentinel non disponible: ECOS-CLI introuvable ou incomplet")
    print(f"   Erreur: {e}")
    print(f"   Chemin recherché: {ecos_cli_path}")

    # Classes stub pour éviter les erreurs d'import
    class _StubClass:
        def __init__(self, *args, **kwargs):
            raise ImportError("GitSentinel requires ECOS-CLI to be available")

    GitSentinelCitizen = _StubClass
    SyncOrchestrator = _StubClass
    ConflictResolver = _StubClass
    CommitValidator = _StubClass
    BranchManager = _StubClass
    SecurityAuditor = _StubClass
    PerformanceOptimizer = _StubClass
    PredictiveAnalyzer = _StubClass
    FederationManager = _StubClass

    __all__ = []
