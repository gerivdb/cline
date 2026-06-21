"""
Types ECOS - Définitions de types communes pour l'écosystème ECOS
Types de données, interfaces et structures partagées.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime

@dataclass
class PhiImpact:
    """
    Impact φ (Phi) d'une opération ou d'un citoyen.

    Représente l'impact positif ou négatif sur l'écosystème ECOS.
    """
    impact: float  # Valeur entre -1.0 et +1.0
    reason: str   # Explication de l'impact

    def __post_init__(self):
        if not -1.0 <= self.impact <= 1.0:
            raise ValueError(f"Impact φ doit être entre -1.0 et 1.0, reçu: {self.impact}")

@dataclass
class CitizenContext:
    """
    Contexte d'exécution pour un citoyen.

    Contient toutes les informations nécessaires à l'exécution
    d'une mission par un citoyen.
    """
    citizen_id: str
    mission_type: str
    parameters: Dict[str, Any]
    environment: Dict[str, Any]
    timestamp: datetime
    priority: int = 1  # 1-10, 10 étant la plus haute priorité
    timeout_seconds: Optional[int] = None

    def __post_init__(self):
        if not 1 <= self.priority <= 10:
            raise ValueError("La priorité doit être entre 1 et 10")

@dataclass
class OperationResult:
    """
    Résultat d'une opération exécutée par un citoyen.
    """
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    phi_impact: Optional[PhiImpact] = None

@dataclass
class ValidationResult:
    """
    Résultat d'une validation constitutionnelle.
    """
    passed: bool
    violations: List[str] = None
    recommendations: List[str] = None
    score: float = 0.0  # Score de conformité 0.0-1.0

    def __post_init__(self):
        if self.violations is None:
            self.violations = []
        if self.recommendations is None:
            self.recommendations = []
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Le score doit être entre 0.0 et 1.0")

@dataclass
class SyncOperation:
    """
    Opération de synchronisation Git.
    """
    operation_type: str  # 'pull', 'push', 'merge', 'fetch'
    repository_path: str
    branch: str = "main"
    remote: str = "origin"
    force: bool = False
    options: Dict[str, Any] = None

    def __post_init__(self):
        if self.options is None:
            self.options = {}

@dataclass
class ConflictResolution:
    """
    Résolution d'un conflit Git.
    """
    conflict_file: str
    strategy: str  # 'auto', 'manual', 'ours', 'theirs'
    resolved_content: Optional[str] = None
    backup_created: bool = True

# Types pour les analyses prédictives
PredictionResult = Dict[str, Any]
RiskAssessment = Dict[str, Any]

# Types pour les métriques de performance
PerformanceMetrics = Dict[str, float]
SystemHealth = Dict[str, Any]

# Types pour la gestion fédérée
FederationConfig = Dict[str, Any]
RepositoryState = Dict[str, Any]

# Constantes communes
PHI_MAX_IMPACT = 1.0
PHI_MIN_IMPACT = -1.0
DEFAULT_PRIORITY = 5
MAX_TIMEOUT_SECONDS = 3600  # 1 heure

# Énumérations sous forme de chaînes pour compatibilité
CITIZEN_STATUS_INITIALIZED = "initialized"
CITIZEN_STATUS_ACTIVE = "active"
CITIZEN_STATUS_IDLE = "idle"
CITIZEN_STATUS_ERROR = "error"
CITIZEN_STATUS_SHUTDOWN = "shutdown"

OPERATION_STATUS_PENDING = "pending"
OPERATION_STATUS_RUNNING = "running"
OPERATION_STATUS_COMPLETED = "completed"
OPERATION_STATUS_FAILED = "failed"
OPERATION_STATUS_CANCELLED = "cancelled"

VALIDATION_STATUS_PASSED = "passed"
VALIDATION_STATUS_FAILED = "failed"
VALIDATION_STATUS_WARNING = "warning"
