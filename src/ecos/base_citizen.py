"""
Base Citizen - Classe de base pour tous les citoyens ECOS
Fournit l'interface commune et les fonctionnalités de base.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseCitizen(ABC):
    """
    Classe de base abstraite pour tous les citoyens ECOS.

    Tous les citoyens doivent hériter de cette classe et implémenter
    les méthodes abstraites.
    """

    def __init__(self, citizen_id: str):
        self.citizen_id = citizen_id
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        self.status = "initialized"
        self.metadata: Dict[str, Any] = {}

        logger.info(f"🧬 Citoyen {citizen_id} initialisé")

    @property
    @abstractmethod
    def phi_impact(self) -> float:
        """
        Impact φ (Phi) de ce citoyen sur l'écosystème.

        Returns:
            Valeur entre 0.0 et 1.0 représentant l'impact φ
        """
        pass

    @abstractmethod
    async def execute_mission(self, context) -> Any:
        """
        Mission principale du citoyen.

        Args:
            context: Contexte d'exécution

        Returns:
            Résultat de la mission (généralement PhiImpact)
        """
        pass

    async def get_status(self) -> Dict[str, Any]:
        """
        Retourne le statut actuel du citoyen.

        Returns:
            Dictionnaire contenant le statut
        """
        return {
            "citizen_id": self.citizen_id,
            "status": self.status,
            "phi_impact": self.phi_impact,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "metadata": self.metadata
        }

    async def update_activity(self):
        """Met à jour le timestamp de dernière activité."""
        self.last_active = datetime.utcnow()

    def set_metadata(self, key: str, value: Any):
        """Définit une valeur dans les métadonnées."""
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur des métadonnées."""
        return self.metadata.get(key, default)

    async def shutdown(self):
        """Arrêt propre du citoyen."""
        self.status = "shutdown"
        logger.info(f"🛑 Citoyen {self.citizen_id} arrêté")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.citizen_id} phi={self.phi_impact}>"
