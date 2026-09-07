from datetime import datetime

from clases.cancha import Cancha, EstadoOperativo
from clases.excepciones import CanchaNoDisponibleError, HorarioNoPermitidoError, OperacionNoAutorizadaError
from clases.roles import RolAdministrador, RolCapitan, RolEstudiante
from clases.usuario import Usuario


def separador(titulo):
    print(f"\n=== {titulo} ===")


def main():
    cancha_futbol = Cancha("C-01", "Futbol")
    cancha_basquet = Cancha("C-02", "Basquet")
    cancha_tenis = Cancha("C-03", "Tenis")

    ana = Usuario("U-01", "Ana", RolEstudiante())
    luis = Usuario("U-02", "Luis", RolCapitan())
    marco = Usuario("U-03", "Marco", RolAdministrador())

    # ---------------- Flujo 1: Reservar Cancha ----------------
    separador("A1: Estudiante intenta reservar antes de las 18:00")
    hora_pico = datetime(2026, 9, 7, 16, 0)
    try:
        ana.solicitar_reserva("R-01", cancha_futbol, hora_pico)
    except HorarioNoPermitidoError as e:
        print(f"Resultado: {e}")

    separador("A2: Capitan reserva antes de las 18:00 (tiene prioridad)")
    reserva_luis = luis.solicitar_reserva("R-02", cancha_futbol, hora_pico)

    separador("A3: Otro usuario intenta reservar la misma cancha ya ocupada")
    hora_alterna = datetime(2026, 9, 7, 17, 0)
    try:
        marco.solicitar_reserva("R-03", cancha_futbol, hora_alterna)
    except CanchaNoDisponibleError as e:
        print(f"Resultado: {e}")

    separador("A4: Estudiante reserva a las 19:00 (fuera de la franja restringida)")
    hora_libre = datetime(2026, 9, 7, 19, 0)
    reserva_ana = ana.solicitar_reserva("R-04", cancha_basquet, hora_libre)

    separador("A5: Reserva sobre cancha en Mantenimiento")
    cancha_tenis.estado_operativo = EstadoOperativo.MANTENIMIENTO
    try:
        luis.solicitar_reserva("R-05", cancha_tenis, hora_pico)
    except CanchaNoDisponibleError as e:
        print(f"Resultado: {e}")

    # ---------------- Flujo 2: Cancelar Reserva ----------------
    separador("B1: Cancelacion con 2h o más de anticipación -> Cancelada")
    hora_actual = datetime(2026, 9, 7, 13, 0)
    luis.cancelar_reserva(reserva_luis, hora_actual)

    separador("B2: La cancha liberada vuelve a estar disponible")
    reserva_marco = marco.solicitar_reserva("R-06", cancha_futbol, hora_alterna)

    separador("B3: Cancelacion con menos de 2h de anticipación -> No-Show")
    hora_actual_tarde = datetime(2026, 9, 7, 18, 30)
    ana.cancelar_reserva(reserva_ana, hora_actual_tarde)

    separador("B4: Usuario intenta cancelar una reserva ajena")
    try:
        luis.cancelar_reserva(reserva_marco, hora_actual)
    except OperacionNoAutorizadaError as e:
        print(f"Resultado: {e}")

    # ---------------- Flujo 3: Gestionar Canchas ----------------
    separador("C1: Un no-Administrador intenta modificar el estado de una cancha")
    try:
        ana.cambiar_estado_cancha(cancha_tenis, EstadoOperativo.DISPONIBLE)
    except OperacionNoAutorizadaError as e:
        print(f"Resultado: {e}")

    separador("C2: El Administrador modifica el estado operativo de la cancha")
    marco.cambiar_estado_cancha(cancha_tenis, EstadoOperativo.DISPONIBLE)

    # ---------------- Flujo 4: Intervenir Conflictos Reservas ----------------
    separador("D1: El Administrador anula una reserva por conflicto")
    marco.anular_reserva_por_conflicto(reserva_marco)


if __name__ == "__main__":
    main()
