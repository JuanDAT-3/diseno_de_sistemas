from fabricas.personaje_factory import PersonajeFactory
from abc import ABC, abstractmethod

# Clase abstracta de fábrica de mundos
class MundoFactory(ABC):
    @abstractmethod
    def crear_jugador(self):
        pass

    @abstractmethod
    def crear_enemigo(self):
        pass

    @abstractmethod
    def nombre_mundo(self):
        pass



class FantasyFactory(MundoFactory):
    def crear_jugador(self):
        return PersonajeFactory.crear("guerrero")

    def crear_enemigo(self):
        return PersonajeFactory.crear("dragon")

    def nombre_mundo(self):
        return "Fantasía"


class SciFiFactory(MundoFactory):
    def crear_jugador(self):
        return PersonajeFactory.crear("soldado")

    def crear_enemigo(self):
        return PersonajeFactory.crear("alien")

    def nombre_mundo(self):
        return "Ciencia Ficción"