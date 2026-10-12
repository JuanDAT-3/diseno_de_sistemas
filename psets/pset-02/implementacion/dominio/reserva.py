from abc import ABC, abstractmethod
from datetime import datetime, time

from dominio.estados import EstadoReserva
from dominio.franja import Franja
from strategy.politicas_cancelacion import PoliticaAnulacionAdministrativa, PoliticaCancelacion


class Reserva(ABC):
    tipo = "Reserva"

    def __init__(self, id_reserva: str, franja: Franja, usuario_propietario, cancha_asignada,
                 politica: PoliticaCancelacion, equipo=None, notas: str = ""):
        self.id_reserva = id_reserva
        self.franja = franja
        self.usuario_propietario = usuario_propietario
        self.cancha_asignada = cancha_asignada
        self.politica = politica
        self.equipo = list(equipo or [])
        self.notas = notas
        self.estado = EstadoReserva.ACTIVA

    @property
    def hora_inicio(self) -> datetime:
        return self.franja.inicio

    @property
    def activa(self) -> bool:
        return self.estado is EstadoReserva.ACTIVA

    def procesar_cancelacion(self, ahora: datetime, politica: PoliticaCancelacion = None) -> EstadoReserva:
        politica = politica or self.politica
        self.estado = politica.determinar_estado(self.hora_inicio, ahora)
        return self.estado

    def anular_por_administrador(self, ahora: datetime) -> EstadoReserva:
        return self.procesar_cancelacion(ahora, PoliticaAnulacionAdministrativa())

    def marcar_desplazada(self) -> None:
        self.estado = EstadoReserva.DESPLAZADA_POR_PRIORIDAD

    @abstractmethod
    def puede_ser_desplazada_por(self, rol, hora_solicitada: time) -> bool:
        raise NotImplementedError

    def __str__(self):
        return (f"{self.id_reserva} [{self.tipo}] {self.usuario_propietario.nombre} "
                f"{self.cancha_asignada.id_cancha} {self.franja} ({self.estado.value})")


class ReservaRegular(Reserva):
    tipo = "Regular"

    def puede_ser_desplazada_por(self, rol, hora_solicitada: time) -> bool:
        return rol.tiene_prioridad(hora_solicitada)


class ReservaEquipoOficial(Reserva):
    tipo = "Equipo oficial"

    def puede_ser_desplazada_por(self, rol, hora_solicitada: time) -> bool:
        return False
