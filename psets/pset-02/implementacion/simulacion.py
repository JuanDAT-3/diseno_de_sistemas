import threading
from datetime import date, datetime, time

from prototype.bloqueo import Bloqueo
from dominio.cancha import Cancha, EstadoOperativo
from singleton.configuracion import ConfiguracionReglas
from dominio.excepciones import (CanchaNoDisponibleError, ConflictoRecurrenteError, HorarioNoPermitidoError,
                                OperacionNoAutorizadaError, ReservaRecurrenteInvalidaError, SolicitanteSuspendidoError)
from facade.reservau_facade import ReservaUFacade
from builder.reserva_recurrente import ReservaRecurrenteBuilder
from dominio.roles import RolAdministrador, RolCapitan, RolEstudiante
from utilidades.salida import imprimir
from abstract_factory.sedes import FabricaCampusNorte, FabricaCampusSur, Sede
from dominio.usuario import Usuario

# ----------------- Funciones auxiliares -----------------
def separador(titulo):
    imprimir(f"\n=== {titulo} ===")


def intentar(funcion, *errores):
    """Ejecuta una operacion de la Facade e imprime su resultado, sea exito o rechazo. Proteger contra errores esperados"""
    try:
        return funcion()
    except errores as e:
        imprimir(f"  Resultado: {e}")
        return None


def main():
    # ---------------- Preparacion ----------------
    separador("Preparación: configuración única, sedes, canchas y usuarios")
    config = ConfiguracionReglas() # Singleton
    
    # Configuración de sdedes
    norte = Sede(FabricaCampusNorte())
    sur = Sede(FabricaCampusSur())
    n1 = Cancha("N-01", "Futbol", norte)
    n2 = Cancha("N-02", "Basquet", norte)
    n3 = Cancha("N-03", "Tenis", norte)
    s1 = Cancha("S-01", "Futbol", sur)

    # Usuarios
    ana = Usuario("U-01", "Ana", RolEstudiante())
    bruno = Usuario("U-02", "Bruno", RolEstudiante())
    diego = Usuario("U-03", "Diego", RolEstudiante())
    elena = Usuario("U-04", "Elena", RolEstudiante())
    luis = Usuario("U-05", "Luis", RolCapitan())
    marta = Usuario("U-06", "Marta", RolCapitan())
    marco = Usuario("U-07", "Marco", RolAdministrador())

    # Facade
    fachada = ReservaUFacade()
    hoy = datetime(2026, 10, 10, 9, 0)

    # ---------------- Escenario 1 ----------------
    separador("Escenario 1: una reserva en cada sede, validada y notificada por su sede")
    reserva_ana = fachada.reservar(ana, n1, datetime(2026, 10, 12, 10, 0), hoy)
    reserva_bruno = fachada.reservar(bruno, s1, datetime(2026, 10, 12, 10, 0), hoy)

    # ---------------- Escenario 2 ----------------
    separador("Escenario 2: reserva rechazada por horario de la sede (Sur abre a las 07:00)")
    intentar(lambda: fachada.reservar(ana, s1, datetime(2026, 10, 12, 6, 30), hoy),
             HorarioNoPermitidoError)
    separador("Escenario 2b: la misma hora sí es válida en Campus Norte (abre a las 06:00)")
    fachada.reservar(elena, n3, datetime(2026, 10, 12, 6, 30), hoy)

        # ---------------- Escenario 3 ----------------
    separador("Escenario 3a: reserva recurrente exitosa (Luis, 4 semanas, con equipo y nota)")
    builder_luis = (ReservaRecurrenteBuilder(luis, n2, date(2026, 10, 19), time(17, 0), time(18, 0))
                    .con_semanas(4)
                    .con_equipo(["balones", "chalecos"])
                    .con_notas("Entrenamiento de la seleccion"))
    recurrentes_luis = fachada.reservar_recurrente(builder_luis, hoy)

    separador("Escenario 3b: reserva recurrente rechazada por conflicto (Marta choca en la semana 2)")
    builder_marta = ReservaRecurrenteBuilder(marta, n2, date(2026, 10, 12), time(17, 0), time(18, 0)).con_semanas(4)
    intentar(lambda: fachada.reservar_recurrente(builder_marta, hoy), ConflictoRecurrenteError)
    imprimir("  Verificación todo-o-nada: reservas activas en N-02 después del rechazo:")
    for r in fachada.reservas_activas(n2):
        imprimir(f"    {r}")

    separador("Escenario 3c: reserva recurrente con semanas fuera de rango (9 semanas)")
    builder_9 = ReservaRecurrenteBuilder(marta, n2, date(2026, 11, 2), time(17, 0), time(18, 0)).con_semanas(9)
    intentar(lambda: fachada.reservar_recurrente(builder_9, hoy), ReservaRecurrenteInvalidaError)

    separador("Escenario 3d: un estudiante intenta una reserva recurrente (solo los capitanes pueden)")
    builder_ana = ReservaRecurrenteBuilder(ana, n2, date(2026, 11, 9), time(17, 0), time(18, 0)).con_semanas(3)
    intentar(lambda: fachada.reservar_recurrente(builder_ana, hoy), OperacionNoAutorizadaError)
    
    # ---------------- Escenario 4 ----------------
    separador("Escenario 4a: estudiante cancela con tiempo (3 h de anticipación) -> Cancelada")
    fachada.cancelar(ana, reserva_ana, datetime(2026, 10, 12, 7, 0))

    separador("Escenario 4b: capitán cancela con menos de 24 h -> No-Show")
    fachada.cancelar(luis, recurrentes_luis[0], datetime(2026, 10, 19, 9, 0))

    separador("Escenario 4c: el administrador anula una reserva -> sin penalidad")
    fachada.cancelar(marco, reserva_bruno, datetime(2026, 10, 12, 9, 30))
    imprimir(f"  Verificación: no-shows de Bruno = {len(bruno.no_shows)}")

    # ---------------- Escenario 5 ----------------
    separador("Escenario 5: Diego acumula 3 no-shows en el mes y luego intenta reservar")
    #Creación de reservas de Diego
    horas = [12, 13, 14]
    reservas_diego = [fachada.reservar(diego, n3, datetime(2026, 10, 13, h, 0), hoy) for h in horas]

    # Cancelació  de las 3 resevas de Diego 30 minutos antes de la hora de inicio (No-Show)
    for reserva, h in zip(reservas_diego, horas):
        imprimir(f"\n  -- Diego cancela {reserva.id_reserva} 30 minutos antes --")
        fachada.cancelar(diego, reserva, datetime(2026, 10, 13, h - 1, 30))
    
    #Comprobación de que Diego está suspendido
    imprimir("\n  -- Diego intenta reservar estando suspendido --")
    intentar(lambda: fachada.reservar(diego, n3, datetime(2026, 10, 21, 10, 0),
                                                           datetime(2026, 10, 13, 15, 0)),
             SolicitanteSuspendidoError)

    
    # ---------------- Escenario 6 ----------------
    separador("Escenario 6: bloqueo clonado en dos canchas, una con una reserva existente")
    fachada.reservar(ana, n1, datetime(2026, 10, 14, 15, 0), hoy)
    # Creación de Bloqueo (Prototype)
    plantilla = Bloqueo("Torneo interfacultades", time(15, 0), time(17, 0), ["red", "balones"])
    clon_prueba = plantilla.clonar(n3, date(2026, 10, 14))
    clon_prueba.equipo.append("conos")
    imprimir(f"\n Prototype: equipo del clon = {clon_prueba.equipo} | equipo de la plantilla = {plantilla.equipo}")
    fachada.bloquear(marco, plantilla, [n1, n2], [date(2026, 10, 14)], hoy)

    # ---------------- Extra: prioridad (RF-03) ----------------
    separador("Extra (RF-03): un capitán antes de las 18:00 desplaza la reserva de un estudiante")
    fachada.reservar(ana, n3, datetime(2026, 10, 15, 10, 0), hoy)
    fachada.reservar(luis, n3, datetime(2026, 10, 15, 10, 0), hoy)

    # ---------------- Extra: Gestionar canchas ----------------
    separador("Extra (Gestionar canchas): un no-administrador intenta cambiar el estado de una cancha")
    intentar(lambda: ana.cambiar_estado_cancha(n3, EstadoOperativo.MANTENIMIENTO), OperacionNoAutorizadaError)

    separador("Extra (Gestionar canchas): el administrador pone N-03 en mantenimiento y se rechaza una reserva")
    marco.cambiar_estado_cancha(n3, EstadoOperativo.MANTENIMIENTO)
    intentar(lambda: fachada.reservar(bruno, n3, datetime(2026, 10, 16, 10, 0), hoy), CanchaNoDisponibleError)
    marco.cambiar_estado_cancha(n3, EstadoOperativo.DISPONIBLE)

    # ---------------- Escenario 7 ----------------
    separador("Escenario 7: dos hilos reservan la misma cancha y franja al mismo tiempo")
    inicio = datetime(2026, 10, 20, 19, 0)
    resultados = {}
    barrera = threading.Barrier(2, timeout=5)
    fachada.punto_sincronizacion = barrera.wait  # ambos hilos ven la franja libre antes de que alguno registre

    def reservar_en_hilo(usuario):
        try:
            r = fachada.reservar(usuario, n3, inicio, hoy)
            resultados[usuario.nombre] = f"CONFIRMADA ({r.id_reserva})"
        except CanchaNoDisponibleError as e:
            resultados[usuario.nombre] = f"RECHAZADA ({e})"

    hilos = [threading.Thread(target=reservar_en_hilo, args=(u,), name=u.nombre) for u in (ana, elena)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    fachada.punto_sincronizacion = None

    imprimir("  Resultado por hilo:")
    for nombre, resultado in sorted(resultados.items()):
        imprimir(f"    {nombre}: {resultado}")
    confirmadas = [r for r in fachada.reservas_activas(n3) if r.franja.inicio == inicio]
    imprimir(f"  Reservas confirmadas para {n3.id_cancha} el {inicio:%Y-%m-%d %H:%M}: {len(confirmadas)}")


if __name__ == "__main__":
    main()
