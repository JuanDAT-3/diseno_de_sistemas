from enum import Enum

from concurrencia.calendario import CalendarioCancha
from abstract_factory.sedes import Sede


class EstadoOperativo(Enum):
    DISPONIBLE = "Disponible"
    MANTENIMIENTO = "Mantenimiento"


class Cancha:
    def __init__(self, id_cancha: str, deporte: str, sede: Sede,
                 estado_operativo: EstadoOperativo = EstadoOperativo.DISPONIBLE):
        self.id_cancha = id_cancha
        self.deporte = deporte
        self.sede = sede
        self.estado_operativo = estado_operativo
        self.calendario = CalendarioCancha()

    def esta_operativa(self) -> bool:
        return self.estado_operativo is EstadoOperativo.DISPONIBLE

    def verificar_disponibilidad(self, franja, rol):
        return self.calendario.evaluar(franja, rol)

    def cambiar_estado_operativo(self, nuevo_estado: EstadoOperativo) -> None:
        self.estado_operativo = nuevo_estado

    def __str__(self):
        return f"Cancha {self.id_cancha} ({self.deporte}, {self.sede.nombre})"
