import threading

_candado = threading.Lock()


def imprimir(texto: str) -> None:
    """print atomico: evita que las lineas de dos hilos se mezclen."""
    with _candado:
        print(texto, flush=True)
