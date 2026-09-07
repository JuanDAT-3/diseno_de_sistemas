from datetime import datetime

from .excepciones import CanchaNoDisponibleError, HorarioNoPermitidoError, OperacionNoAutorizadaError
from .reserva import Reserva
from .roles import Rol, RolAdministrador


class Usuario:
    def __init__(self, id_usuario: str, nombre: str, rol_activo: Rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.rol_activo = rol_activo

    def solicitar_reserva(self, id_reserva: str, cancha, hora_solicitada: datetime) -> Reserva:
        print(f"1. {self.nombre} solicita reservar la cancha {cancha.id_cancha} para las {hora_solicitada:%H:%M}")

        print(f"2. El sistema valida el horario mediante el rol activo ({self.rol_activo})")
        if not self.rol_activo.validar_horario(hora_solicitada.time()):
            print("3. Horario no permitido -> se lanza HorarioNoPermitidoError")
            raise HorarioNoPermitidoError(
                f"{self.nombre} ({self.rol_activo}) no puede reservar a las {hora_solicitada:%H:%M}"
            )

        print("3. Horario permitido, el sistema verifica la disponibilidad de la cancha")
        if not cancha.verificar_disponibilidad():
            print("4. Cancha no disponible -> se lanza CanchaNoDisponibleError")
            raise CanchaNoDisponibleError(f"La cancha {cancha.id_cancha} no está disponible")

        print("4. Cancha disponible, el sistema crea la reserva y asocia la cancha")
        reserva = Reserva(id_reserva, hora_solicitada, self, cancha)

        print(f"5. El sistema confirma la reserva: {reserva}")
        return reserva

    def cancelar_reserva(self, reserva: Reserva, hora_actual: datetime):
        print(f"1. {self.nombre} solicita cancelar la reserva {reserva.id_reserva}")

        print("2. El sistema valida que el usuario solicitante sea el propietario de la reserva")
        if reserva.usuario_propietario.id_usuario != self.id_usuario:
            print("3. Usuario no autorizado -> se lanza OperacionNoAutorizadaError")
            raise OperacionNoAutorizadaError(f"{self.nombre} no puede cancelar una reserva que no le pertenece")

        print("3. Usuario autorizado, el sistema invoca reserva.procesar_cancelacion(hora_actual)")
        estado = reserva.procesar_cancelacion(hora_actual)

        print(f"4. La reserva actualiza su estado a {estado.value} y libera la cancha")
        return estado

    def cambiar_estado_cancha(self, cancha, nuevo_estado):
        print(f"1. {self.nombre} solicita modificar el estado operativo de la cancha {cancha.id_cancha}")
        print(f"2. El sistema verifica el rol de {self.nombre} ({self.rol_activo})")
        if not isinstance(self.rol_activo, RolAdministrador):
            print("3. No es Administrador -> el sistema niega el acceso")
            raise OperacionNoAutorizadaError(f"{self.nombre} no tiene permisos de Administrador")

        print("3. Es Administrador, el sistema permite modificar el estado operativo")
        self.rol_activo.cambiar_estado_cancha(cancha, nuevo_estado)
        print(f"4. El sistema actualiza el estado operativo de la cancha a {nuevo_estado.value}")

    def anular_reserva_por_conflicto(self, reserva):
        print(f"1. {self.nombre} solicita anular la reserva {reserva.id_reserva} por conflicto")
        if not isinstance(self.rol_activo, RolAdministrador):
            raise OperacionNoAutorizadaError(f"{self.nombre} no tiene permisos de Administrador")
        self.rol_activo.anular_reserva_por_conflicto(reserva)

    def __str__(self):
        return f"{self.nombre} ({self.rol_activo})"
