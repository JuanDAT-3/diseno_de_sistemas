import copy
from datetime import date, datetime, time

from dominio.franja import Franja


class Bloqueo:
    """Se define una vez como plantilla y se clona por cancha y fecha."""

    def __init__(self, motivo: str, hora_inicio: time, hora_fin: time, equipo: list):
        self.motivo = motivo
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.equipo = list(equipo)
        self.cancha = None
        self.fecha = None

    def clonar(self, cancha, fecha: date) -> "Bloqueo":
        # deepcopy: 'equipo' es una lista mutable; con copy.copy el clon compartiria
        # la misma lista con la plantilla y modificarla en uno alteraria el otro.
        clon = copy.deepcopy(self)
        clon.cancha = cancha
        clon.fecha = fecha
        return clon

    @property
    def franja(self) -> Franja:
        return Franja(datetime.combine(self.fecha, self.hora_inicio),
                      datetime.combine(self.fecha, self.hora_fin))
