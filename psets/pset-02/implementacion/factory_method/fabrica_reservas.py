from abc import ABC, abstractmethod

from strategy.politicas_cancelacion import PoliticaCancelacionCapitan, PoliticaCancelacionEstudiante
from dominio.reserva import Reserva, ReservaEquipoOficial, ReservaRegular


class CreadorReserva(ABC):
    """La decision de que clase instanciar vive solo aqui."""

    def crear(self, id_reserva, solicitante, cancha, franja, equipo=None, notas="") -> Reserva:
        return self._instanciar(id_reserva, solicitante, cancha, franja, equipo, notas)

    @abstractmethod
    def _instanciar(self, id_reserva, solicitante, cancha, franja, equipo, notas) -> Reserva:
        raise NotImplementedError


class CreadorReservaRegular(CreadorReserva):
    def _instanciar(self, id_reserva, solicitante, cancha, franja, equipo, notas):
        return ReservaRegular(id_reserva, franja, solicitante, cancha,
                              PoliticaCancelacionEstudiante(), equipo, notas)


class CreadorReservaEquipoOficial(CreadorReserva):
    def _instanciar(self, id_reserva, solicitante, cancha, franja, equipo, notas):
        return ReservaEquipoOficial(id_reserva, franja, solicitante, cancha,
                                    PoliticaCancelacionCapitan(), equipo, notas)
