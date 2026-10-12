from enum import Enum


class EstadoReserva(Enum):
    ACTIVA = "Activa"
    CANCELADA = "Cancelada"
    NO_SHOW = "No-Show"
    ANULADA_POR_ADMIN = "AnuladaPorAdmin"
    DESPLAZADA_POR_PRIORIDAD = "DesplazadaPorPrioridad"
