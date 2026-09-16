class ReglaDeNegocioError(Exception):
    pass


class HorarioNoPermitidoError(ReglaDeNegocioError):
    pass


class CanchaNoDisponibleError(ReglaDeNegocioError):
    pass


class OperacionNoAutorizadaError(ReglaDeNegocioError):
    pass
