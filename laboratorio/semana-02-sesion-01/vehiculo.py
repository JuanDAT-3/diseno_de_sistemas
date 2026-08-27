#Vehiculo -> Mover()

# Auto -> Por carretera.
# 
# Bote -> por agua.
# 
# Avion -> por aire.  


#---------------------------------------------------------------
# Clase Vehiculo
class Vehiculo:
    def __init__(self, Comportamiento_Movimiento):
        self.comportamiento_movimiento = Comportamiento_Movimiento
    
    def mover():
        self.comportamiento_movimiento.mover() 

#---------------------------------------------------------------
# Clase ComportamientoMovimiento
class ComportamientoMovimiento():
    def mover(self):
        raise NotImplementedError("Este método debe ser implementado por la subclase.") # Error de implementación.

class PorCarretera(ComportamientoMovimiento):
    def mover(self):
        print("Conduciendo por carretera.")

class PorAgua(ComportamientoMovimiento):
    def mover(self):
        print("Navegando por agua.")

class PorAire(ComportamientoMovimiento):
    def mover(self):
        print("Volando por aire.")

#---------------------------------------------------------------
# Clases Vehiculos

class auto(Vehiculo):
    def __init__(self, Comportamiento_Movimiento):
        super().__init__(Comportamiento_Movimiento)
    
    def mover(self):
        self.comportamiento_movimiento.mover()

class bote(Vehiculo):
    def __init__(self, Comportamiento_Movimiento):
        super().__init__(Comportamiento_Movimiento)
    
    def mover(self):
        self.comportamiento_movimiento.mover()

class avion(Vehiculo):
    def __init__(self, Comportamiento_Movimiento):
        super().__init__(Comportamiento_Movimiento)
    
    def mover(self):
        self.comportamiento_movimiento.mover()

#---------------------------------------------------------------
# Main

if __name__ == "__main__":
    auto = auto(PorCarretera())
    auto.mover()

    print()

    bote = bote(PorAgua())
    bote.mover()

    print()

    avion = avion(PorAire())
    avion.mover()

    print()
    