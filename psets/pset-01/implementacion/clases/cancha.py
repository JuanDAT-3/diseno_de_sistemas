from enum import Enum


class EstadoOperativo(Enum):
    DISPONIBLE = "Disponible"
    MANTENIMIENTO = "Mantenimiento"


class Cancha:
    def __init__(self, id_cancha: str, deporte: str,
                 estado_operativo: EstadoOperativo = EstadoOperativo.DISPONIBLE):
        self.id_cancha = id_cancha
        self.deporte = deporte
        self.estado_operativo = estado_operativo
        self._ocupada = False

    def verificar_disponibilidad(self) -> bool:
        return self.estado_operativo == EstadoOperativo.DISPONIBLE and not self._ocupada

    def ocupar(self):
        self._ocupada = True

    def liberar(self):
        self._ocupada = False

    def cambiar_estado_operativo(self, nuevo_estado: EstadoOperativo):
        self.estado_operativo = nuevo_estado

    def __str__(self):
        return f"Cancha({self.id_cancha}, {self.deporte}, {self.estado_operativo.value})"
