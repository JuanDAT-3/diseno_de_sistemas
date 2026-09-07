from datetime import datetime, timedelta
from enum import Enum


class EstadoReserva(Enum):
    ACTIVA = "Activa"
    CANCELADA = "Cancelada"
    NO_SHOW = "No-Show"
    ANULADA_POR_ADMIN = "AnuladaPorAdmin"


class Reserva:
    LIMITE_CANCELACION = timedelta(hours=2)

    def __init__(self, id_reserva: str, hora_inicio: datetime, usuario_propietario, cancha_asignada):
        self.id_reserva = id_reserva
        self.hora_inicio = hora_inicio
        self.estado = EstadoReserva.ACTIVA
        self.usuario_propietario = usuario_propietario
        self.cancha_asignada = cancha_asignada
        self.cancha_asignada.ocupar()

    def procesar_cancelacion(self, hora_actual: datetime) -> EstadoReserva:
        tiempo_restante = self.hora_inicio - hora_actual
        if tiempo_restante < self.LIMITE_CANCELACION:
            self.estado = EstadoReserva.NO_SHOW
        else:
            self.estado = EstadoReserva.CANCELADA
        self.cancha_asignada.liberar()
        return self.estado

    def anular_por_administrador(self) -> EstadoReserva:
        print("2. El sistema cambia el estado de la reserva a 'AnuladaPorAdmin'")
        self.estado = EstadoReserva.ANULADA_POR_ADMIN
        self.cancha_asignada.liberar()
        print("3. El sistema libera la cancha asociada")
        return self.estado

    def __str__(self):
        return (f"Reserva({self.id_reserva}, {self.hora_inicio:%Y-%m-%d %H:%M}, "
                f"estado={self.estado.value}, cancha={self.cancha_asignada.id_cancha})")
