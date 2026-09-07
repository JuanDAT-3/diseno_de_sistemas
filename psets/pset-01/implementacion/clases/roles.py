from abc import ABC
from datetime import time

from .reglas_prioridad import PrioridadAntesDeLas18, PrioridadTotal, ReglaPrioridad, SinPrioridad


class Rol(ABC):
    HORA_LIMITE = time(18, 0)

    def __init__(self, tipo_rol: str, regla_prioridad: ReglaPrioridad):
        self.tipo_rol = tipo_rol
        self._regla_prioridad = regla_prioridad

    def validar_horario(self, hora_solicitada: time) -> bool:
        if hora_solicitada >= self.HORA_LIMITE:
            return True
        return self._regla_prioridad.tiene_prioridad(hora_solicitada)

    def __str__(self):
        return self.tipo_rol


class RolEstudiante(Rol):
    def __init__(self):
        super().__init__("Estudiante", SinPrioridad())


class RolCapitan(Rol):
    def __init__(self):
        super().__init__("Capitan", PrioridadAntesDeLas18())


class RolAdministrador(Rol):
    def __init__(self):
        super().__init__("Administrador", PrioridadTotal())

    def cambiar_estado_cancha(self, cancha, nuevo_estado):
        cancha.cambiar_estado_operativo(nuevo_estado)

    def anular_reserva_por_conflicto(self, reserva):
        reserva.anular_por_administrador()
