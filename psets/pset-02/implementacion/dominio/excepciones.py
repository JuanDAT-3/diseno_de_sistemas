class ReglaDeNegocioError(Exception):
    pass


class HorarioNoPermitidoError(ReglaDeNegocioError):
    pass


class CanchaNoDisponibleError(ReglaDeNegocioError):
    pass


class OperacionNoAutorizadaError(ReglaDeNegocioError):
    pass


class SolicitanteSuspendidoError(ReglaDeNegocioError):
    pass


class ReservaNoActivaError(ReglaDeNegocioError):
    pass


class ReservaRecurrenteInvalidaError(ReglaDeNegocioError):
    pass


class ConflictoRecurrenteError(ReglaDeNegocioError):
    def __init__(self, semana: int, motivo: str):
        super().__init__(f"Conflicto en la semana {semana}: {motivo}")
        self.semana = semana
