from abc import ABC
from datetime import time

from factory_method.fabrica_reservas import CreadorReserva, CreadorReservaEquipoOficial, CreadorReservaRegular
from strategy.reglas_prioridad import PrioridadAntesDeLas18, ReglaPrioridad, SinPrioridad


class Rol(ABC):
    puede_intervenir_reservas = False
    puede_reservar_recurrente = False

    def __init__(self, tipo_rol: str, regla_prioridad: ReglaPrioridad, creador_reserva: CreadorReserva):
        self.tipo_rol = tipo_rol
        self._regla_prioridad = regla_prioridad
        self.creador_reserva = creador_reserva

    def tiene_prioridad(self, hora_solicitada: time) -> bool:
        return self._regla_prioridad.tiene_prioridad(hora_solicitada)

    def __str__(self):
        return self.tipo_rol


class RolEstudiante(Rol):
    def __init__(self):
        super().__init__("Estudiante", SinPrioridad(), CreadorReservaRegular())


class RolCapitan(Rol):
    puede_reservar_recurrente = True
    def __init__(self):
        super().__init__("Capitan", PrioridadAntesDeLas18(), CreadorReservaEquipoOficial())


class RolAdministrador(Rol):
    puede_intervenir_reservas = True

    def __init__(self):
        super().__init__("Administrador", SinPrioridad(), CreadorReservaRegular())

    def cambiar_estado_cancha(self, cancha, nuevo_estado):
        cancha.cambiar_estado_operativo(nuevo_estado)
