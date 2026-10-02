from config.game_config import GameConfig
from fabricas.mundo_factory import FantasyFactory, SciFiFactory
from estrategias.estrategia import AtaqueNormal, AtaqueFuerte

class GameFacade:
    # Estado Inicial 
    def __init__(self):
        self.game_config = GameConfig()
        self.mundo = None
        self.jugador = None
        self.enemigo = None
        self.estrategia = AtaqueNormal() 
        self.turno = 0
        self.ganador = None
    
    def seleccionar_mundo(self, opcion: int):
        if opcion == 1:
            self.mundo = FantasyFactory().nombre_mundo()
            self.jugador = FantasyFactory().crear_jugador()
            self.enemigo = FantasyFactory().crear_enemigo()
        elif opcion == 2:
            self.mundo = SciFiFactory().nombre_mundo()
            self.jugador = SciFiFactory().crear_jugador()
            self.enemigo = SciFiFactory().crear_enemigo()
        else:
            raise ValueError("Opción de mundo inválida")
        
    
    def seleccionar_estrategia(self, opcion: int):
        if opcion == 1:
            self.estrategia = AtaqueNormal()
        elif opcion == 2:
            self.estrategia = AtaqueFuerte()
        else:
            raise ValueError("Opción de estrategia inválida")
    
    # Juego
    def ejecutar_turno(self):
        self.turno += 1
        resultado = {
            "turno": self.turno,
            "acciones": [],
            "ganador": None,
        }

        # Ataque del jugador 
        danio = self.estrategia.atacar(self.jugador, self.enemigo)
        if danio == 0:
            resultado["acciones"].append(
                f"{self.jugador.nombre} falló su ataque."
            )
        else:
            resultado["acciones"].append(
                f"{self.jugador.nombre} usó {self.estrategia.nombre()} "
                f"y causó {danio} de daño a {self.enemigo.nombre}."
            )

        if not self.enemigo.esta_vivo():
            self.ganador = self.jugador.nombre
            resultado["ganador"] = self.ganador
            return resultado

        # Respuesta del enemigo
        contra = AtaqueNormal()
        danio_enemigo = contra.atacar(self.enemigo, self.jugador)
        if danio_enemigo == 0:
            resultado["acciones"].append(
                f"{self.enemigo.nombre} falló su ataque."
            )
        else:
            resultado["acciones"].append(
                f"{self.enemigo.nombre} respondió y causó "
                f"{danio_enemigo} de daño a {self.jugador.nombre}."
            )

        if not self.jugador.esta_vivo():
            self.ganador = self.enemigo.nombre
            resultado["ganador"] = self.ganador

        return resultado

    def esta_terminado(self):
        return (
            self.turno >= self.game_config.numero_maximo_turnos
            or not self.jugador.esta_vivo()
            or not self.enemigo.esta_vivo()
        )

    def obtener_ganador(self):
        return self.ganador

    def obtener_estado(self):
        return {
            "config": str(self.game_config),
            "mundo": self.mundo if self.mundo else "—",
            "jugador": str(self.jugador) if self.jugador else "—",
            "enemigo": str(self.enemigo) if self.enemigo else "—",
            "turno": self.turno,
            "max_turnos": self.game_config.numero_maximo_turnos,
        }