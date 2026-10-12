import threading
from enum import Enum

from dominio.excepciones import CanchaNoDisponibleError, ConflictoRecurrenteError
from dominio.franja import Franja


class EvaluacionFranja(Enum):
    LIBRE = "libre"
    DESPLAZABLE = "ocupada por reservas desplazables por prioridad"
    OCUPADA = "ocupada"
    BLOQUEADA = "bloqueada por un evento"


class CalendarioCancha:
    """Franjas ocupadas y bloqueadas de una cancha."""

    def __init__(self):
        self._reservas = []
        self._bloqueos = []
        self._candado = threading.Lock()

    # ---- helpers internos ----
    def _conflictos(self, franja: Franja):
        return [r for r in list(self._reservas) if r.activa and r.franja.se_solapa(franja)]

    def _esta_bloqueada(self, franja: Franja) -> bool:
        return any(b.franja.se_solapa(franja) for b in list(self._bloqueos))

    def _evaluar(self, franja, rol, hora) -> EvaluacionFranja:
        if self._esta_bloqueada(franja):
            return EvaluacionFranja.BLOQUEADA
        conflictos = self._conflictos(franja)
        if not conflictos:
            return EvaluacionFranja.LIBRE
        if all(c.puede_ser_desplazada_por(rol, hora) for c in conflictos):
            return EvaluacionFranja.DESPLAZABLE
        return EvaluacionFranja.OCUPADA

    # ---- consultas  ----
    def evaluar(self, franja: Franja, rol) -> EvaluacionFranja:
        return self._evaluar(franja, rol, franja.inicio.time())

    def esta_libre(self, franja: Franja) -> bool:
        return not self._esta_bloqueada(franja) and not self._conflictos(franja)

    def reservas_activas(self):
        return [r for r in list(self._reservas) if r.activa]

    # ---- escrituras (lock) ----
    def registrar(self, reserva, rol):
        """Verifica y registra de forma atómica. Devuelve las reservas desplazadas por prioridad."""
        with self._candado:
            evaluacion = self._evaluar(reserva.franja, rol, reserva.franja.inicio.time())
            if evaluacion in (EvaluacionFranja.OCUPADA, EvaluacionFranja.BLOQUEADA):
                raise CanchaNoDisponibleError(
                    f"La cancha {reserva.cancha_asignada.id_cancha} ya no está disponible en {reserva.franja}")
            desplazadas = self._conflictos(reserva.franja)
            for r in desplazadas:
                r.marcar_desplazada()
            self._reservas.append(reserva)
            return desplazadas

    def registrar_lote(self, reservas) -> None:
        """Todo o nada: si una semana choca, no se registra ninguna."""
        with self._candado:
            for semana, reserva in enumerate(reservas, start=1):
                if self._esta_bloqueada(reserva.franja) or self._conflictos(reserva.franja):
                    raise ConflictoRecurrenteError(semana, "la franja ya no está libre")
            self._reservas.extend(reservas)

    def liberar(self, reserva) -> None:
        with self._candado:
            if reserva in self._reservas:
                self._reservas.remove(reserva)

    def aplicar_bloqueo(self, bloqueo, ahora):
        """Anula las reservas de la franja (sin penalidad) y registra el bloqueo.
        Devuelve la lista de reservas anuladas, o None si la franja ya estaba bloqueada."""
        with self._candado:
            if self._esta_bloqueada(bloqueo.franja):
                return None
            afectadas = self._conflictos(bloqueo.franja)
            for r in afectadas:
                r.anular_por_administrador(ahora)
            self._bloqueos.append(bloqueo)
            return afectadas
