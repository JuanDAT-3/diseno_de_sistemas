from facade.game_facade import GameFacade

juego = GameFacade()

# Elegir mundo
juego.seleccionar_mundo(1)

# Ver estado inicial
estado = juego.obtener_estado()
print(f"Mundo: {estado['mundo']}")
print(f"Jugador: {estado['jugador']}")
print(f"Enemigo: {estado['enemigo']}")

# 3) Bucle de turnos
while not juego.esta_terminado():
    opcion = int(input("Estrategia (1=Normal, 2=Fuerte): "))
    juego.seleccionar_estrategia(opcion)

    resultado = juego.ejecutar_turno()
    for accion in resultado["acciones"]:
        print(accion)

# 4) Fin
ganador = juego.obtener_ganador()
if ganador:
    print(f"Ganador: {ganador}")
else:
    print("Empate")