from abc import ABC, abstractmethod
from datetime import datetime

from singleton.configuracion import ConfiguracionReglas
from dominio.estados import EstadoReserva


class PoliticaCancelacion(ABC):
    """Decide en que estado queda una reserva al cancelarse."""

    nombre = ""

    @abstractmethod
    def determinar_estado(self, inicio: datetime, ahora: datetime) -> EstadoReserva:
        raise NotImplementedError


class PoliticaCancelacionEstudiante(PoliticaCancelacion):
    nombre = "Estudiante (ventana de 2 h)"

    def determinar_estado(self, inicio, ahora):
        ventana = ConfiguracionReglas().ventana_cancelacion_estudiante
        return EstadoReserva.NO_SHOW if inicio - ahora < ventana else EstadoReserva.CANCELADA


class PoliticaCancelacionCapitan(PoliticaCancelacion):
    nombre = "Capitan (ventana de 24 h)"

    def determinar_estado(self, inicio, ahora):
        ventana = ConfiguracionReglas().ventana_cancelacion_capitan
        return EstadoReserva.NO_SHOW if inicio - ahora < ventana else EstadoReserva.CANCELADA


class PoliticaAnulacionAdministrativa(PoliticaCancelacion):
    nombre = "Anulación administrativa (sin penalidad)"

    def determinar_estado(self, inicio, ahora):
        return EstadoReserva.ANULADA_POR_ADMIN
