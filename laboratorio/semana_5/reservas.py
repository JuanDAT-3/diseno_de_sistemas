class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre
    

class EquipoOficial:
    def __init__(self, nombre):
        self.nombre = nombre

def reservar_desde_web(nombre_cancha, fecha, hora_inicio, hora_fin,solicitante):
    creador = FabricadeResevas().elegir_creador(solicitante)
    reserva = creador.crear_reserva(nombre_cancha, fecha, hora_inicio, hora_fin, solicitante)
    return reserva

class ReservaRegular:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante
    
    def confirmar(self):
        return "Reserva regular confirmada."
    
class ReservaPrioritaria:
    def __init__(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.solicitante = solicitante
    
    def confirmar(self):
        return "Reserva prioritaria confirmada."
# -----------------------------------
class CreadorDeReserva(): # Molde de como crar la fabrica (Factory Method) 
    def crear_reserva(self, chancha, fecha, hora_inicio, hora_fin, solicitante):
        raise NotImplementedError('')
        

class CreadordeReservaRegular(CreadorDeReserva):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaRegular(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )

class CreadorDeReservaPrioritaria(CreadorDeReserva):
    def crear_reserva(self, cancha, fecha, hora_inicio, hora_fin, solicitante):
        return ReservaPrioritaria(
            cancha,
            fecha,
            hora_inicio,
            hora_fin,
            solicitante
        )

class FabricadeResevas():
    @staticmethod
    def elegir_creador(solicitante):
        if isinstance(solicitante, Estudiante):
            return CreadordeReservaRegular()
        elif isinstance(solicitante, EquipoOficial):
            return CreadorDeReservaPrioritaria()
# -----------------------------------
def main():
    reserva_1 = reservar_desde_web(
        'cancha de futbol',
        '2026-09-17',
        '18:00',
        '20:00',
        Estudiante('Erick')
    )

    print(reserva_1.confirmar())

    reserva_2 = reservar_desde_web(
        'cancha de futbol',
        '2026-09-17',
        '18:00',
        '20:00',
        EquipoOficial('Erick Capitan')
    )

    print(reserva_2.confirmar())

if __name__ == '__main__':
    main()  