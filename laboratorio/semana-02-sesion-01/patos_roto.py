
#---------------------------------------------------------------
class ComportamientoVuelo(): #Clase abstacta, Interfaz o "molde"
    def volar(self):
        raise NotImplementedError("Este método debe ser implementado por la subclase.") # Raise para hacer que salte una excepcion de implementación.

class VuelaconAlas(ComportamientoVuelo):
    def volar(self):
        print("Volando con alas.")

class NoVuela(ComportamientoVuelo):
    def volar(self):
        print("No vuela.")
#---------------------------------------------------------------
class ComportamientoGraznido(): #Clase abstacta, Interfaz o "molde"
    def graznar(self):
        raise NotImplementedError("Este método debe ser implementado por la subclase.") # Raise para hacer que salte una excepcion de implementación.
    
class GraznidoNormal(ComportamientoGraznido):
    def graznar(self):
        print("Cuac!")

class GraznidoDeGoma(ComportamientoGraznido):
    def graznar(self):
        print("Chirrido de Goma.")

#---------------------------------------------------------------
class Pato: 
    def __init__(self, Comportamiento_Vuelo, Comportamiento_Graznido):
        self.comportamiento_vuelo = Comportamiento_Vuelo
        self.comportamiento_graznido = Comportamiento_Graznido

    def nadar(self,):
        print("Nadando.")
    
    def graznar(self):
        self.comportamiento_graznido.graznar()

    def volar(self):
        self.comportamiento_vuelo.volar() #Delegación de la responsabilidad de volar a la clase ComportamientoVuelo.


class PatoSalvaje(Pato):
    def __init__(self, Comportamiento_Vuelo, Comportamiento_Graznido):
        super().__init__(Comportamiento_Vuelo, Comportamiento_Graznido)
       
    pass ## Pasa todo lo de la clase padre. 

class PatoDeGoma(Pato):
    def __init__(self, Comportamiento_Vuelo, Comportamiento_Graznido):
        super().__init__(Comportamiento_Vuelo, Comportamiento_Graznido)
    def graznar(self):
        self.comportamiento_graznido.graznar()

    def volar(self):
        self.comportamiento_vuelo.volar()

#------------------------------------------------------------------
if __name__ == "__main__":
    salvaje = PatoSalvaje(VuelaconAlas(), GraznidoNormal())
    salvaje.nadar()
    salvaje.graznar()
    salvaje.volar()

    print()

    de_goma = PatoDeGoma(NoVuela(), GraznidoDeGoma())
    de_goma.nadar()
    de_goma.graznar()
    de_goma.volar()

    print()