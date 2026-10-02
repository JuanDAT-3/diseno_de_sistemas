# Clase Padre Personaje
class Personaje:
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    def recibir_danio(self, danio : int):
        self.vida = max(0, self.vida - danio)
    
    def esta_vivo(self):
        return self.vida > 0

    def __str__(self):
        return f"{self.nombre} (vida: {self.vida}, ataque: {self.ataque})"

# Clases Hijas 
## Guerrero
class Guerrero(Personaje):
    def __init__(self):
        super().__init__("Guerrero", vida = 120, ataque = 35)
    
class Dragon(Personaje):
    def __init__(self):
        super().__init__("Dragón", vida=200, ataque=25)


class Soldado(Personaje):
    def __init__(self):
        super().__init__("Soldado", vida=110, ataque=40)


class Alien(Personaje):
    def __init__(self):
        super().__init__("Alien", vida=100, ataque=50)