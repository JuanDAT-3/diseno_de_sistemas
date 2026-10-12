from datetime import datetime, timedelta

from dominio.excepciones import OperacionNoAutorizadaError
from singleton.configuracion import ConfiguracionReglas
from utilidades.salida import imprimir
from dominio.roles import Rol


class Usuario:
    def __init__(self, id_usuario: str, nombre: str, rol_activo: Rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.rol_activo = rol_activo
        self.no_shows: list[datetime] = []
        self.suspendido_hasta: datetime | None = None

    def no_shows_del_mes(self, ahora: datetime) -> int:
        return sum(1 for f in self.no_shows if (f.year, f.month) == (ahora.year, ahora.month))

    def registrar_no_show(self, ahora: datetime) -> bool:
        """Registra un no-show y suspende si llega al limite del mes. True si quedo suspendido."""
        config = ConfiguracionReglas()
        self.no_shows.append(ahora)
        if self.no_shows_del_mes(ahora) >= config.max_no_shows_mes:
            self.suspendido_hasta = ahora + timedelta(days=config.dias_suspension)
            return True
        return False

    def esta_suspendido(self, ahora: datetime) -> bool:
        return self.suspendido_hasta is not None and ahora < self.suspendido_hasta

    def cambiar_estado_cancha(self, cancha, nuevo_estado):
        imprimir(f"1. {self.nombre} solicita modificar el estado operativo de la cancha {cancha.id_cancha}")
        imprimir(f"2. El sistema verifica el rol de {self.nombre} ({self.rol_activo})")
        if not self.rol_activo.puede_intervenir_reservas:
            imprimir("3. No es Administrador -> el sistema niega el acceso")
            raise OperacionNoAutorizadaError(f"{self.nombre} no tiene permisos de Administrador")

        imprimir("3. Es Administrador, el sistema permite modificar el estado operativo")
        self.rol_activo.cambiar_estado_cancha(cancha, nuevo_estado)
        imprimir(f"4. El sistema actualiza el estado operativo de la cancha a {nuevo_estado.value}")

    def __str__(self):
        return f"{self.nombre} ({self.rol_activo})"
