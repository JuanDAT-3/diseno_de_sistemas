import itertools

from concurrencia.calendario import EvaluacionFranja
from singleton.configuracion import ConfiguracionReglas
from dominio.estados import EstadoReserva
from dominio.excepciones import (CanchaNoDisponibleError, ConflictoRecurrenteError, HorarioNoPermitidoError,
                          OperacionNoAutorizadaError, ReservaNoActivaError, ReservaRecurrenteInvalidaError,
                          SolicitanteSuspendidoError)
from dominio.franja import Franja
from strategy.politicas_cancelacion import PoliticaAnulacionAdministrativa
from utilidades.salida import imprimir


class ReservaUFacade:
    """Facade: unica puerta de entrada para reservar, reservar de forma recurrente, cancelar y bloquear.
    Coordina disponibilidad/calendario, sede, registro de no-shows y notificacion."""

    def __init__(self):
        self._config = ConfiguracionReglas()
        self._ids = itertools.count(1)
        self.punto_sincronizacion = None  # gancho para la simulacion de concurrencia

    def _nuevo_id(self) -> str:
        return f"R-{next(self._ids):02d}"

     # Función auxiliar de seguimiento de pasos.
    def _paso(self, usuario, numero, texto: str) -> None:
        imprimir(f"  [{usuario.nombre}] {numero}. {texto}")

    def reservas_activas(self, cancha):
        return cancha.calendario.reservas_activas()

    # ---------------- Reservar una cancha ----------------
    def reservar(self, solicitante, cancha, inicio, ahora, fin=None):
        franja = Franja(inicio, fin or inicio + self._config.duracion_reserva)
        sede = cancha.sede

        self._paso(solicitante, 1, f"{solicitante} solicita reservar {cancha} para {franja}")

        self._paso(solicitante, 2, "El sistema verifica que el solicitante no esté suspendido")
        if solicitante.esta_suspendido(ahora):
            self._paso(solicitante, "2a",
                       f"Solicitante suspendido hasta {solicitante.suspendido_hasta:%Y-%m-%d %H:%M} -> solicitud rechazada")
            raise SolicitanteSuspendidoError(f"{solicitante.nombre} está suspendido")

        self._paso(solicitante, 3, f"El sistema valida el horario permitido de {sede.nombre}")
        if not sede.validador_horario.es_valido(franja):
            self._paso(solicitante, "3a", f"Horario fuera del permitido en {sede.nombre} -> solicitud rechazada")
            raise HorarioNoPermitidoError(f"{franja} está fuera del horario de {sede.nombre}")

        self._paso(solicitante, 4, "El sistema verifica que la cancha esté operativa y la franja disponible")
        if not cancha.esta_operativa():
            self._paso(solicitante, "4a", "Cancha en mantenimiento -> solicitud rechazada")
            raise CanchaNoDisponibleError(f"{cancha.id_cancha} está en mantenimiento")
        evaluacion = cancha.verificar_disponibilidad(franja, solicitante.rol_activo)
        if evaluacion is EvaluacionFranja.BLOQUEADA:
            self._paso(solicitante, "4b", "Franja bloqueada por un evento -> solicitud rechazada")
            raise CanchaNoDisponibleError(f"{cancha.id_cancha} está bloqueada en {franja}")
        if evaluacion is EvaluacionFranja.OCUPADA:
            self._paso(solicitante, "4c", "Franja ocupada y sin prioridad para desplazarla -> solicitud rechazada")
            raise CanchaNoDisponibleError(f"{cancha.id_cancha} está ocupada en {franja}")
        if evaluacion is EvaluacionFranja.DESPLAZABLE:
            self._paso(solicitante, 4, "La franja está ocupada por reservas que la prioridad del solicitante puede desplazar")

        reserva = solicitante.rol_activo.creador_reserva.crear(self._nuevo_id(), solicitante, cancha, franja)
        self._paso(solicitante, 5,
                   f"El sistema crea la reserva {reserva.id_reserva} de tipo '{reserva.tipo}' "
                   f"con política de cancelación: {reserva.politica.nombre}")

        if self.punto_sincronizacion:
            self.punto_sincronizacion()

        try:
            desplazadas = cancha.calendario.registrar(reserva, solicitante.rol_activo)
        except CanchaNoDisponibleError:
            self._paso(solicitante, "6a", "Otra solicitud confirmó la franja primero -> solicitud rechazada")
            raise
        self._paso(solicitante, 6, f"El sistema registra la reserva {reserva.id_reserva} en el calendario de {cancha.id_cancha}")
        for r in desplazadas:
            self._paso(solicitante, "6b",
                       f"Reserva {r.id_reserva} de {r.usuario_propietario.nombre} desplazada por prioridad (sin penalidad)")
            sede.notificador.notificar(
                r.usuario_propietario, f"Su reserva {r.id_reserva} fue desplazada por prioridad de un equipo oficial")

        self._paso(solicitante, 7, "El sistema notifica la confirmación por el canal de la sede")
        sede.notificador.notificar(solicitante, f"Reserva {reserva.id_reserva} confirmada: {cancha.id_cancha}, {franja}")
        return reserva

    # ---------------- Reservar de forma recurrente ----------------
    def reservar_recurrente(self, builder, ahora):
        solicitante, cancha = builder.solicitante, builder.cancha
        sede = cancha.sede

        self._paso(solicitante, 1, f"{solicitante} solicita una reserva recurrente en {cancha}")

        self._paso(solicitante, 2, "El sistema verifica que el solicitante sea capitán y no esté suspendido")
        if not solicitante.rol_activo.puede_reservar_recurrente:
            self._paso(solicitante, "2b", "El solicitante no es capitán -> solicitud rechazada")
            raise OperacionNoAutorizadaError(f"{solicitante.nombre} no puede crear reservas recurrentes")
        if solicitante.esta_suspendido(ahora):
            self._paso(solicitante, "2a", "Solicitante suspendido -> solicitud rechazada")
            raise SolicitanteSuspendidoError(f"{solicitante.nombre} está suspendido")

        self._paso(solicitante, 3, "El sistema construye la solicitud validando que las semanas estén entre "
                                   f"{self._config.semanas_min} y {self._config.semanas_max}")
        try:
            solicitud = builder.construir()
        except ReservaRecurrenteInvalidaError as e:
            self._paso(solicitante, "3a", f"{e} -> solicitud rechazada")
            raise

        self._paso(solicitante, 4, "El sistema verifica que la cancha esté operativa y, semana por semana, "
                                   "el horario de la sede y la disponibilidad")
        if not cancha.esta_operativa():
            self._paso(solicitante, "4c", "Cancha en mantenimiento -> solicitud rechazada")
            raise CanchaNoDisponibleError(f"{cancha.id_cancha} está en mantenimiento")
        for semana, franja in enumerate(solicitud.franjas, start=1):
            self._paso(solicitante, 4, f"Semana {semana}: horario de sede y disponibilidad ({franja})")
            if not sede.validador_horario.es_valido(franja):
                self._paso(solicitante, "4b",
                           f"Semana {semana} fuera del horario de {sede.nombre} -> no se registra ninguna semana")
                raise ConflictoRecurrenteError(semana, "fuera del horario permitido de la sede")
            if not cancha.calendario.esta_libre(franja):
                self._paso(solicitante, "4a",
                           f"Semana {semana} choca con otra reserva -> no se registra ninguna semana")
                raise ConflictoRecurrenteError(semana, "la cancha no está disponible")

        reservas = [
            solicitante.rol_activo.creador_reserva.crear(self._nuevo_id(), solicitante, cancha, franja,
                                                  solicitud.equipo, solicitud.notas)
            for franja in solicitud.franjas
        ]
        try:
            cancha.calendario.registrar_lote(reservas)
        except ConflictoRecurrenteError as e:
            self._paso(solicitante, "5a", f"{e} (concurrencia) -> no se registra ninguna semana")
            raise
        self._paso(solicitante, 5, f"El sistema registra las {len(reservas)} reservas "
                                   f"({reservas[0].id_reserva} a {reservas[-1].id_reserva}) de forma atómica")

        self._paso(solicitante, 6, "El sistema notifica la confirmación por el canal de la sede")
        extras = ""
        if solicitud.equipo:
            extras += f" Equipo prestado: {', '.join(solicitud.equipo)}."
        if solicitud.notas:
            extras += f" Notas de la reserva: {solicitud.notas}"
        sede.notificador.notificar(solicitante, f"{len(reservas)} reservas recurrentes confirmadas en {cancha.id_cancha}.{extras}")
        return reservas

    # ---------------- Cancelar una reserva ----------------
    def cancelar(self, solicitante, reserva, ahora):
        self._paso(solicitante, 1, f"{solicitante} solicita cancelar la reserva {reserva.id_reserva}")

        self._paso(solicitante, 2, "El sistema valida que el solicitante sea el propietario o el administrador")
        es_propietario = reserva.usuario_propietario.id_usuario == solicitante.id_usuario
        if not es_propietario and not solicitante.rol_activo.puede_intervenir_reservas:
            self._paso(solicitante, "2a", "Usuario no autorizado -> solicitud rechazada")
            raise OperacionNoAutorizadaError(f"{solicitante.nombre} no puede cancelar una reserva ajena")
        if not reserva.activa:
            self._paso(solicitante, "2b", f"La reserva ya está en estado {reserva.estado.value} -> solicitud rechazada")
            raise ReservaNoActivaError(f"La reserva {reserva.id_reserva} no está activa")

        politica = reserva.politica if es_propietario else PoliticaAnulacionAdministrativa()
        self._paso(solicitante, 3, f"El sistema obtiene la política de cancelación: {politica.nombre}")

        restante = reserva.franja.inicio - ahora
        horas = restante.total_seconds() / 3600
        self._paso(solicitante, 4, f"El sistema calcula el tiempo restante hasta el inicio: {horas:.1f} h")

        estado = reserva.procesar_cancelacion(ahora, politica)
        self._paso(solicitante, 5, f"El sistema aplica la política y determina el resultado: {estado.value}")

        reserva.cancha_asignada.calendario.liberar(reserva)
        self._paso(solicitante, 6, f"El sistema registra el estado y libera la franja de {reserva.cancha_asignada.id_cancha}")

        propietario = reserva.usuario_propietario
        if estado is EstadoReserva.NO_SHOW:
            suspendido = propietario.registrar_no_show(ahora)
            self._paso(solicitante, 7,
                       f"El sistema registra el no-show de {propietario.nombre} "
                       f"({propietario.no_shows_del_mes(ahora)} en el mes)")
            if suspendido:
                self._paso(solicitante, "7a",
                           f"{propietario.nombre} llega al límite de no-shows del mes -> suspendido hasta "
                           f"{propietario.suspendido_hasta:%Y-%m-%d %H:%M}")
        else:
            self._paso(solicitante, 7, "Sin penalidad: no se registra no-show")

        self._paso(solicitante, 8, "El sistema notifica el resultado por el canal de la sede")
        reserva.cancha_asignada.sede.notificador.notificar(
            propietario, f"Su reserva {reserva.id_reserva} quedó en estado {estado.value}")
        return estado

    # ---------------- Bloquear canchas para un evento ----------------
    def bloquear(self, administrador, plantilla, canchas, fechas, ahora):
        self._paso(administrador, 1,
                   f"{administrador} define el bloqueo '{plantilla.motivo}' "
                   f"({plantilla.hora_inicio:%H:%M}-{plantilla.hora_fin:%H:%M}, equipo: {', '.join(plantilla.equipo)})")

        self._paso(administrador, 2, "El sistema verifica que el solicitante sea administrador")
        if not administrador.rol_activo.puede_intervenir_reservas:
            self._paso(administrador, "2a", "No es administrador -> solicitud rechazada")
            raise OperacionNoAutorizadaError(f"{administrador.nombre} no puede crear bloqueos")

        self._paso(administrador, 3, f"El administrador elige {len(canchas)} cancha(s) y {len(fechas)} fecha(s)")
        bloqueos = []
        for cancha in canchas:
            for fecha in fechas:
                bloqueo = plantilla.clonar(cancha, fecha)
                self._paso(administrador, 4, f"El sistema clona la plantilla para {cancha.id_cancha} el {fecha}")
                afectadas = cancha.calendario.aplicar_bloqueo(bloqueo, ahora)
                if afectadas is None:
                    self._paso(administrador, "7a", f"{cancha.id_cancha} ya estaba bloqueada en esa franja -> se omite")
                    continue
                if afectadas:
                    self._paso(administrador, 5, f"El sistema encuentra {len(afectadas)} reserva(s) en la franja de {cancha.id_cancha}")
                    for r in afectadas:
                        self._paso(administrador, 6,
                                   f"Reserva {r.id_reserva} de {r.usuario_propietario.nombre} anulada sin penalidad ({r.estado.value})")
                else:
                    self._paso(administrador, 5, f"No hay reservas existentes en la franja de {cancha.id_cancha}")
                    self._paso(administrador, "5a", "Sin reservas que anular -> pasa al paso 7")
                self._paso(administrador, 7, f"El sistema registra el bloqueo en el calendario de {cancha.id_cancha}")
                for r in afectadas:
                    self._paso(administrador, 8, f"El sistema notifica a {r.usuario_propietario.nombre}")
                    cancha.sede.notificador.notificar(
                        r.usuario_propietario,
                        f"Su reserva {r.id_reserva} fue anulada por el bloqueo '{bloqueo.motivo}' (sin penalidad)")
                bloqueos.append(bloqueo)
        return bloqueos
