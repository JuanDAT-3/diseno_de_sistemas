from personajes.personaje import (Guerrero, Dragon, Soldado, Alien)

# Clase Fabrica de personajes
class PersonajeFactory:
    @staticmethod
    def crear(tipo : str):
        tipo = tipo.lower()
        
        if tipo == "guerrero":
            return Guerrero()
        elif tipo == "dragon":
            return Dragon()
        elif tipo == "soldado":
            return Soldado()
        elif tipo == "alien":
            return Alien()
        else:
            raise ValueError(f"Tipo de personaje desconocido: {tipo}")