from abc import ABC, abstractmethod
from datetime import time

from dominio.franja import Franja
from utilidades.salida import imprimir


# ---- Productos abstractos de la familia ----
class ValidadorHorario(ABC):
    @abstractmethod
    def es_valido(self, franja: Franja) -> bool:
        raise NotImplementedError


class Notificador(ABC):
    @abstractmethod
    def notificar(self, destinatario, mensaje: str) -> None:
        raise NotImplementedError


# ---- Productos de Campus Norte ----
class ValidadorHorarioNorte(ValidadorHorario):
    APERTURA = time(6, 0)
    CIERRE = time(22, 0)

    def es_valido(self, franja):
        return self.APERTURA <= franja.inicio.time() and franja.fin.time() <= self.CIERRE


class NotificadorCorreoInstitucional(Notificador):
    def notificar(self, destinatario, mensaje):
        imprimir(f"      [Correo institucional -> {destinatario.nombre}] {mensaje}")


# ---- Productos de Campus Sur ----
class ValidadorHorarioSur(ValidadorHorario):
    APERTURA = time(7, 0)
    CIERRE = time(23, 0)

    def es_valido(self, franja):
        return self.APERTURA <= franja.inicio.time() and franja.fin.time() <= self.CIERRE


class NotificadorMensajeTexto(Notificador):
    def notificar(self, destinatario, mensaje):
        imprimir(f"      [Mensaje de texto -> {destinatario.nombre}] {mensaje}")


# ---- Abstract Factory ----
class FabricaSede(ABC):
    nombre = ""

    @abstractmethod
    def crear_validador_horario(self) -> ValidadorHorario:
        raise NotImplementedError

    @abstractmethod
    def crear_notificador(self) -> Notificador:
        raise NotImplementedError


class FabricaCampusNorte(FabricaSede):
    nombre = "Campus Norte"

    def crear_validador_horario(self):
        return ValidadorHorarioNorte()

    def crear_notificador(self):
        return NotificadorCorreoInstitucional()


class FabricaCampusSur(FabricaSede):
    nombre = "Campus Sur"

    def crear_validador_horario(self):
        return ValidadorHorarioSur()

    def crear_notificador(self):
        return NotificadorMensajeTexto()


class Sede:
    """El cliente solo obtiene validador y notificador a traves de la sede:
    ambos salen de la misma fabrica, no se pueden mezclar entre sedes."""

    def __init__(self, fabrica: FabricaSede):
        self.nombre = fabrica.nombre
        self.validador_horario = fabrica.crear_validador_horario()
        self.notificador = fabrica.crear_notificador()
