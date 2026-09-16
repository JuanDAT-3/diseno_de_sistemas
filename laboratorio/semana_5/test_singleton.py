from singleton import GestorDeConfiguracion, reserva_permitida

def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True
    assert reserva_permitida(config) is False


def test_reserva_aceptada():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = False
    assert reserva_permitida(config) is True
## Al ser una variable global, la anterior asignación lo fijó como True, y en reserva_permitida no se cambia, por lo que la prueba falla