# ReservaU - Sistema de Reservas Universitarias

Este proyecto contiene la implementación en Python de la capa abstracta de ReservaU. El código refleja las entidades, reglas de negocio y los flujos documentados en los Casos de Uso.

El archivo `simulacion.py` ejecutará todos los escenarios y mostrará los resultados paso a paso en la consola.

### Ejecutar Con Docker.
Abre la terminal en la carpeta principal del proyecto y ejecuta:

 
**1. Construir la imagen**

docker build -t reservau .

**2. Ejecutar el contenedor**

docker run --rm reservau