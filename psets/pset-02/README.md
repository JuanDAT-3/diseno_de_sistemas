# README

# PSet 2: Patrones de Diseño en ReservaU

Nombre: Juan David Aguilar

## Cómo ejecutar

Desde `implementacion/`:

```bash
docker build -t reservau-v2 .
docker run reservau-v2
```

También se puede correr sin Docker con `python simulacion.py`.


## Tabla de patrones

| Patrón | Requerimiento que lo justifica | Problema que resuelve (y qué pasaría sin él) | Clases y métodos |
| --- | --- | --- | --- |
| Factory Method | RF-17 | El tipo de reserva depende de quién la solicita. Sin el patrón, habría un `if` sobre el rol repartido entre la Facade y `Reserva`, y cada reserva tendría que recordar asignarse su política. | `CreadorReserva.crear`, `CreadorReservaRegular`, `CreadorReservaEquipoOficial`; `Rol.creador_reserva` |
| Abstract Factory | RF-15, RF-16, RNF-05 | Cada sede necesita su validador de horario y su notificador, y deben ir siempre juntos. Sin el patrón, un `if sede == ...` por cada uso y la posibilidad de validar con una sede y notificar por la otra. | `FabricaSede`, `FabricaCampusNorte`, `FabricaCampusSur`, `Sede` |
| Builder | RF-07, RF-08, RF-09 | La reserva recurrente mezcla datos obligatorios y opcionales. Sin el patrón, un constructor con muchos parámetros opcionales y la validación de semanas dispersa. | `ReservaRecurrenteBuilder.con_semanas`, `.con_equipo`, `.con_notas`, `.construir`; `SolicitudRecurrente` |
| Prototype | RF-13, RF-14 | El administrador define el bloqueo una vez y lo replica por cancha y fecha. Sin el patrón, se repetiría la construcción manual de cada bloqueo. | `Bloqueo.clonar` |
| Singleton | RNF-04 | Los valores de las reglas deben vivir en un solo lugar. Sin el patrón, los números 18:00, 2 h, 24 h, 3 y 7 estarían repartidos por el código. | `ConfiguracionReglas` |
| Strategy | RF-03, RF-02, RF-06, RF-10 | El comportamiento que varía (prioridad y cancelación) vive en su propia clase. Sin el patrón, `Reserva` y `Rol` tendrían un `if` sobre quién es el solicitante. | `ReglaPrioridad` (`PrioridadAntesDeLas18`, `SinPrioridad`); `PoliticaCancelacion` (`PoliticaCancelacionEstudiante`, `PoliticaCancelacionCapitan`, `PoliticaAnulacionAdministrativa`) |
| Facade | RF-01, RF-02, RF-07, RF-13 | Cuatro operaciones coordinan disponibilidad, calendario, sede, no-shows y notificación. Sin el patrón, `simulacion.py` conocería cada subsistema y su orden de llamada. | `ReservaUFacade.reservar`, `.reservar_recurrente`, `.cancelar`, `.bloquear` |
| Concurrencia (locking pesimista) | RNF-03 | Dos solicitudes simultáneas por la misma cancha y franja deben producir una sola reserva confirmada. Sin el candado, ambas verían la franja libre y ambas se registrarían. | `CalendarioCancha.registrar`, `.registrar_lote`, `.aplicar_bloqueo`, `_candado` |

## Supuestos y decisiones

- **Prioridad del capitán (RF-03).** La interpreto como preferencia sobre los estudiantes en horarios antes de las 18:00: el capitán puede desplazar una reserva de estudiante, que queda en `DesplazadaPorPrioridad`, sin penalidad y con aviso. Nunca se desplaza una `ReservaEquipoOficial`. “Antes de las 18:00” se evalúa sobre la hora de inicio de la franja.
- **Reserva recurrente.** Nunca desplaza a nadie y es todo o nada: si falla una semana (horario de la sede, disponibilidad o concurrencia) no se registra ninguna. Si no se indican semanas, son 2 (el rango permitido es de 2 a 8). Solo la puede crear un capitán (`Rol.puede_reservar_recurrente`).
- **Administrador.** Puede reservar como cualquier usuario.
- **Suspensión.** Se evalúa contra `ahora`: 3 no-shows en el mes calendario del momento de la cancelación suspenden al usuario 7 días.
- **Horarios de la sede.** Viven en los validadores de cada sede (Abstract Factory), no en el Singleton.
- **`ahora` como parámetro.** Los métodos reciben `ahora` en lugar de leer el reloj,con el fin de ejecutar la simulación

## Justificaciones

### Prototype: ¿por qué `copy.deepcopy`?

Se usó `deepcopy` con el objetivo de crear objetos independientes en el bloqueo, que permitan modificarse individualmente sin afectar a la plantilla base. La plantilla base permanece inmutable. De haber usado `copy.copy`, el clon sería un objeto nuevo, pero sus atributos mutables, como la lista `equipo`, seguirían siendo la misma lista que la de la plantilla,ya que esta copia es una referencia al original, y modificarla en un clon afectaría a la plantilla y a las demás copias.

### Singleton: costo-benefico

Principalmente se ganó control sobre los atributos que todo el programa usa, manteniendo centralizados los parámetros importantes del negocio. Esto permite modificarlos en un solo lugar y evitar que existan reglas duplicadas o dos reglas diferentes para una misma situación.

El costo es aceptar un sistema menos flexible en estos parámetros, ya que los parámetros de preferencia no tienen que ser modificados en ejecución para mantener esa lógica del programa sin errores que afectarían al sistema entero.

### Concurrencia: locking pesimista o optimista

El uso del locking pesimista apunta a evitar conflictos en la reserva de canchas. En periodos de alta demanda, como el inicio de cada semestre, es muy probable que varias personas quieran reservar la misma cancha prácticamente al mismo tiempo. Con un locking optimista, varias solicitudes procederían a la vez y las que pierdan fallarían al final y tendrían que reintentar, lo que en esos picos sería ineficiente. Con el locking pesimista, solo una solicitud a la vez entra a verificar y registrar, y las demás ven la franja ocupada, evitando así la duplicación y el conflicto de reservas. Las consultas de disponibilidad, que son mucho más numerosas que las reservas, no toman el candado; solo lo toman la verificación y el registro.