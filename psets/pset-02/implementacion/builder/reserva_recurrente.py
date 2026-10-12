from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

from singleton.configuracion import ConfiguracionReglas
from dominio.excepciones import ReservaRecurrenteInvalidaError
from dominio.franja import Franja


@dataclass
class SolicitudRecurrente:
    solicitante: object
    cancha: object
    franjas: list
    equipo: list
    notas: str


class ReservaRecurrenteBuilder:
    """Builder: obligatorios en el constructor, opcionales encadenados."""

    def __init__(self, solicitante, cancha, fecha_inicio: date, hora_inicio: time, hora_fin: time):
        self.solicitante = solicitante
        self.cancha = cancha
        self._fecha_inicio = fecha_inicio
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin
        self._semanas = None
        self._equipo = []
        self._notas = ""

    def con_semanas(self, semanas: int):
        self._semanas = semanas
        return self

    def con_equipo(self, equipo: list):
        self._equipo = list(equipo)
        return self

    def con_notas(self, notas: str):
        self._notas = notas
        return self

    def construir(self) -> SolicitudRecurrente:
        config = ConfiguracionReglas()
        semanas = self._semanas if self._semanas is not None else config.semanas_min
        if not config.semanas_min <= semanas <= config.semanas_max:
            raise ReservaRecurrenteInvalidaError(
                f"El número de semanas debe estar entre {config.semanas_min} y {config.semanas_max} (recibido: {semanas})")
        franjas = [
            Franja(datetime.combine(self._fecha_inicio + timedelta(weeks=i), self._hora_inicio),
                   datetime.combine(self._fecha_inicio + timedelta(weeks=i), self._hora_fin))
            for i in range(semanas)
        ]
        return SolicitudRecurrente(self.solicitante, self.cancha, franjas, list(self._equipo), self._notas)
