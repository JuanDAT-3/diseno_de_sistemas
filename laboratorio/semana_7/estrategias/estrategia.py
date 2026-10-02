import random 
from abc import ABC, abstractmethod
from src.config.game_config import GameConfig

# Clase Abstracta Estrategia
class Estrategia(ABC):
    @abstractmethod
    def atacar(self, personaje, enemigo):
        pass

    @abstractmethod
    def nombre(self):
        pass

# Clases de Estrategias

class AtaqueNormal(Estrategia):

    def atacar(self, personaje, enemigo):
        probabilidad_fallo = GameConfig().probabilidad_fallo
        if random.random() < probabilidad_fallo:
            return 0
        else:
            danio = personaje.ataque
            enemigo.recibir_danio(danio)
            return danio

    def nombre(self):
        return "Ataque Normal"

class AtaqueFuerte(Estrategia):

    def atacar(self, personaje, enemigo):
        probabilidad_fallo = GameConfig().probabilidad_fallo * 2 # Mayor Probabilidad de fallo
        if random.random() < probabilidad_fallo:
            personaje.recibir_danio(5)  # El personaje recibe penalización por fallo
            return 0
        else:
            danio = int(personaje.ataque * 1.5)
            enemigo.recibir_danio(danio)
            return danio

    def nombre(self):
        return "Ataque Fuerte"