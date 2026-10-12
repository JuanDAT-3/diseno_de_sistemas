from abc import ABC, abstractmethod
from datetime import time

from singleton.configuracion import ConfiguracionReglas


class ReglaPrioridad(ABC):
    """Decide si un solicitante tiene prioridad a una hora dada."""

    @abstractmethod
    def tiene_prioridad(self, hora_solicitada: time) -> bool:
        raise NotImplementedError


class PrioridadAntesDeLas18(ReglaPrioridad):
    def tiene_prioridad(self, hora_solicitada: time) -> bool:
        return hora_solicitada < ConfiguracionReglas().hora_limite_prioridad


class SinPrioridad(ReglaPrioridad):
    def tiene_prioridad(self, hora_solicitada: time) -> bool:
        return False
