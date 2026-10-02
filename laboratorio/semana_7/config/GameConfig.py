class GameConfig:
    # Singleton

    _instancia = None
    ## Valores predeterminados
    dificultad = "normal" 
    numero_maximo_turnos = 15
    probabilidad_fallo = 0.1

    def __new__(cls):
        if cls._instancia is None:
            ## Si no tiene instancia, crea una nueva, sino retorna la existente.
            cls._instancia = super().__new__(cls)
        return cls._instancia
    
    def configurar(self, dificultad, numero_maximo_turnos, probabilidad_fallo):
        self.dificultad = dificultad
        self.numero_maximo_turnos = numero_maximo_turnos
        self.probabilidad_fallo = probabilidad_fallo