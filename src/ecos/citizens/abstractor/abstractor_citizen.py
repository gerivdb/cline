"""
AbstractorCitizen (AlphaOracle) : Orchestrateur souverain de la pureté abstraite (L0→L4)

Garantit que chaque ligne de code dans ECOS est fidèle à une intention souveraine (L0) et respecte la hiérarchie L0 → L1 → L2 → L3 → L4.
"""

from typing import Dict, Any, List
from pathlib import Path
from .abstraction_mapper import AbstractionMapper
from .vertical_validator import VerticalValidator
from .abstraction_healer import AbstractionHealer
from .alpha_metrics import AlphaMetrics

class AbstractorCitizen:
    """Orchestrateur souverain de la pureté abstraite (L0→L4)."""
    
    def __init__(self):
        self.mapper = AbstractionMapper()
        self.validator = VerticalValidator()
        self.healer = AbstractionHealer()
        self.metrics = AlphaMetrics()
    
    async def audit_module(self, module_path: Path) -> Dict[str, Any]:
        """Audite un module et retourne son score de pureté abstraite."""
        levels = self.mapper.detect_abstraction_levels(module_path)
        validation = self.validator.validate_vertical_chain(levels)
        alpha_score = self.metrics.compute_alpha(validation)
        
        return {
            "module": str(module_path),
            "levels_detected": levels,
            "validation": validation,
            "alpha": alpha_score,
            "status": "healthy" if alpha_score >= 0.95 else "needs_healing"
        }
    
    async def heal_module(self, module_path: Path) -> Dict[str, Any]:
        """Corrige automatiquement les dérives d'abstraction."""
        audit = await self.audit_module(module_path)
        if audit["alpha"] < 0.90:
            healed = self.healer.apply_corrections(module_path, audit["validation"])
            return {"action": "healed", "changes": healed}
        return {"action": "no_action_needed"}
    
    async def enforce_l0_coverage(self, root_path: Path) -> List[str]:
        """Génère des intents L0 manquants dans tout le workspace."""
        missing = []
        for py_file in root_path.rglob("*.py"):
            if not self.mapper.has_l0_intent(py_file):
                self.healer.inject_l0_intent(py_file)
                missing.append(str(py_file))
        return missing
