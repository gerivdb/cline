"""
AbstractionMapper : Détecte les niveaux d’abstraction (L0-L4) dans un module Python.
"""

from pathlib import Path
from typing import Dict

class AbstractionMapper:
    def detect_abstraction_levels(self, module_path: Path) -> Dict[int, "AbstractionLevel"]:
        """
        Analyse le fichier et détecte la présence des niveaux L0 à L4.
        Retourne un dict {niveau: AbstractionLevel}.
        """
        # Placeholder : détection naïve par recherche de commentaires spéciaux
        levels = {}
        with open(module_path, "r", encoding="utf-8") as f:
            content = f.read()
            for lvl in range(5):
                marker = f"# L{lvl}:"
                compliant = marker in content
                levels[lvl] = AbstractionLevel(level=lvl, content=marker, compliant=compliant)
        return levels

    def has_l0_intent(self, module_path: Path) -> bool:
        """Vérifie la présence d’un intent L0 dans le fichier."""
        with open(module_path, "r", encoding="utf-8") as f:
            return "# L0:" in f.read()
