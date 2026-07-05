from dataclasses import dataclass
from typing import Dict

@dataclass
class AbstractionLevel:
    level: int  # 0=L0, 1=L1, ..., 4=L4
    content: str
    compliant: bool

@dataclass
class VerticalValidation:
    l0_present: bool
    l1_dag_valid: bool
    l2_protocol_valid: bool
    l3_structure_valid: bool
    l4_implementation_valid: bool
    vertical_drift: float  # 0.0 = parfait, 1.0 = rupture totale

class VerticalValidator:
    def validate_vertical_chain(self, levels: Dict[int, AbstractionLevel]) -> VerticalValidation:
        return VerticalValidation(
            l0_present=levels.get(0, AbstractionLevel(0, "", False)).compliant,
            l1_dag_valid=levels.get(1, AbstractionLevel(1, "", False)).compliant,
            l2_protocol_valid=levels.get(2, AbstractionLevel(2, "", False)).compliant,
            l3_structure_valid=levels.get(3, AbstractionLevel(3, "", False)).compliant,
            l4_implementation_valid=levels.get(4, AbstractionLevel(4, "", False)).compliant,
            vertical_drift=self._compute_drift(levels)
        )
    
    def _compute_drift(self, levels: Dict[int, AbstractionLevel]) -> float:
        # Plus il manque de niveaux, plus le drift est élevé
        present = sum(1 for lvl in levels.values() if lvl.compliant)
        return 1.0 - (present / 5.0)
