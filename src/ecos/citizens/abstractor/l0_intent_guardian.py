"""
L0IntentGuardian : Valide et génère les intents L0 (intention souveraine) pour chaque module.
"""

from pathlib import Path

class L0IntentGuardian:
    def validate_l0(self, module_path: Path) -> bool:
        """Vérifie la présence d’un intent L0 dans le module."""
        with open(module_path, "r", encoding="utf-8") as f:
            return "# L0:" in f.read()

    def inject_l0(self, module_path: Path, intent: str = "Intention souveraine manquante") -> None:
        """Injecte un intent L0 standard si absent."""
        with open(module_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if "# L0:" not in "".join(lines):
            lines.insert(0, f"# L0: {intent}\n")
            with open(module_path, "w", encoding="utf-8") as f2:
                f2.writelines(lines)
