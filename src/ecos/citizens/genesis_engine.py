"""
GenesisEngine : Mécanisme reproductif du Hive Mind

Ce module permet la création dynamique de nouveaux citoyens spécialisés selon les besoins détectés par le Hive Mind.
Il encode la logique d’auto-génération, d’initialisation et d’intégration dans la conscience collective.
"""

from typing import Any, Dict, Callable

class GenesisEngine:
    """
    Générateur de citoyens spécialisés pour l’évolution adaptative du système.
    """
    def __init__(self):
        self.registry: Dict[str, Callable[..., Any]] = {}

    def register_blueprint(self, name: str, constructor: Callable[..., Any]) -> None:
        """Enregistre un blueprint de citoyen spécialisé."""
        self.registry[name] = constructor

    def create_citizen(self, name: str, *args, **kwargs) -> Any:
        """Crée une instance d’un citoyen spécialisé à partir d’un blueprint."""
        if name not in self.registry:
            raise ValueError(f"Blueprint '{name}' non trouvé.")
        return self.registry[name](*args, **kwargs)
