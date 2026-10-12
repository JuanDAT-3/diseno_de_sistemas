from datetime import time, timedelta


class ConfiguracionReglas:
    """unico lugar donde viven los valores de las reglas."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            inst = super().__new__(cls)
            inst.hora_limite_prioridad = time(18, 0)
            inst.ventana_cancelacion_estudiante = timedelta(hours=2)
            inst.ventana_cancelacion_capitan = timedelta(hours=24)
            inst.max_no_shows_mes = 3
            inst.dias_suspension = 7
            inst.semanas_min = 2
            inst.semanas_max = 8
            inst.duracion_reserva = timedelta(hours=1)
            cls._instancia = inst
        return cls._instancia
