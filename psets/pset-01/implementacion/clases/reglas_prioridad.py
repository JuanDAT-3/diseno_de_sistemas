from abc import ABC, abstractmethod
from datetime import time


class ReglaPrioridad(ABC):
    @abstractmethod
    def tiene_prioridad(self, hora_solicitada: time) -> bool:
        raise NotImplementedError


class PrioridadAntesDeLas18(ReglaPrioridad):
    HORA_LIMITE = time(18, 0)

    def tiene_prioridad(self, hora_solicitada: time) -> bool:
        return hora_solicitada < self.HORA_LIMITE


class SinPrioridad(ReglaPrioridad):
    def tiene_prioridad(self, hora_solicitada: time) -> bool:
        return False


class PrioridadTotal(ReglaPrioridad):
    def tiene_prioridad(self, hora_solicitada: time) -> bool:
        return True
