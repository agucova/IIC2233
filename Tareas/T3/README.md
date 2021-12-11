# Tarea 3: DCCalamar :school_satchel:

## Consideraciones generales :octocat:
La tarea implementa el modelo cliente-servidor, el protocolo de comunicación,
el algoritmo de cifrado y la ventana de inicio y de sala de espera. No implementa las partidas en si o el resto de ventanas.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Networking: 23 pts (18%)
##### ✅ Protocolo
##### ✅ Correcto uso de sockets
##### ✅ Conexión
##### ✅ Manejo de clientes
#### Arquitectura Cliente - Servidor: 31 pts (24%)
##### ✅ Roles
##### ✅ Consistencia
##### 🟠 Logs: Se agregó loggeo en toda la funcionalidad implementada.
#### Manejo de Bytes: 20 pts (15%)
##### ✅ Codificación
##### ✅ Decodificación
##### ✅ Encriptación
##### ✅ Integración
#### Interfaz gráfica: 31 pts (24%)
##### 🟠 Modelación: No estoy seguro a que se refiere, pero intenté desligar el front del back-end.
##### ✅ Ventana inicio
##### ✅ Sala Principal
##### ❌ Ventana de Invitación
##### ❌ Sala de juego
##### ❌ Ventana final
#### Reglas de DCCalamar: 21 pts (16%)
##### 🟠 Inicio del juego
##### ❌ Ronda
##### ❌ Termino del juego
#### General: 4 pts (3%)
##### ✅ Parámetros (JSON)
#### Bonus: 5 décimas máximo
##### ❌ Cheatcode
##### ❌ Turnos con tiempo
## Ejecución :computer:
Tanto el cliente como el servidor dependen del paquete propio calamarlib,
que debe estar disponible en el PYTHONPATH. La forma mas fácil de hacerlo es aprovechando pip:
```shell
$ pip install -e calamar_lib/
```
Esto debería instalar el paquete localmente en modo de desarrollo.

Porque no se me ocurrió testear los sprites independiente de mi repo local,
no me di cuenta que la estructura modificada de la carpeta `Sprites` estaba
cubierta por mi `gitignore`. En consecuencia, debe moverse la carpeta `Sprites` a dentro de la carpeta `cliente/` y cambiar `Avatares`, `Decoraciones`, `Juego` y `Logos` a minúscula.

Se puede iniciar el servidor con:
```shell
$ python3 servidor/main.py
```

Y el el cliente con:
```shell
$ python cliente/.py
```

## Librerías :books:
### Librerías externas utilizadas

La lista de paquetes de la librería estándar que utilicé fue las siguientes:

1. `__future__`: se utiliza para proveer type hints de colecciones en formato retrocompatible a 3.8. (`list[str]` en vez de `List[str]` importado de `typing`).
2. `typing`: se utiliza para crear objetos de tipo `NamedTuple` que mejoran la versión incluída en `collection`, permitiendo declarar sus tipos para facilitar análisis estático. También agrega hints como `Union` y `Optional`, para facilitar el tipado.

Ninguna de las dos cambian la ejecución del código, sino que simplemente permiten anotar los tipos del código acorde con [PEP 484](https://www.python.org/dev/peps/pep-0484/), cosa de que mi editor pueda reconocer los tipos normalmente. Consulté por este uso de type hints en tanto Discord como en [issues](https://github.com/IIC2233/Syllabus/issues/31#issuecomment-908031345) en tareas pasadas y me dieron permiso para usarlos.

Además se usó `pickle`, `json` y `socket` de la librería estándar y `PyQt5` como única librería externa.

### Librerías propias
Se creó un paquete compartido `calamarlib` para evitar la duplicación de código, entendido
que si bien el enunciado indicaba que el cliente y el servidor no podían depender mutuamente,
no decía nada en contra de que compartieran código de una tercera carpeta, evitando repetir alrededor de 400 líneas.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Supuse que los sockets del servidor no tenían que necesiamente ser terminados, dado que la combinación del garbage collection, el timeout del kernel y el uso de ADDR_REUSE, permiten que no haya ningún problema práctico.
2. Supuse que el cliente podía conectarse de forma sincrónica con el servidor.
3. Supuse que el contenido de los mensajes entre cliente y servidor quedaba a mi juicio, por lo que implementé un protocolo en base a JSON (también cambiable a `pickle` usando la constante `PROVIDER`).


## Referencias de código externo :book:

Mi mayor referencia fue el [ejemplo de servidor](https://github.com/IIC2233/contenidos/blob/main/semana-12/3-ejemplos.ipynb) con concurrencia en la semana 12 de los contendiso curso.

También tomé la base de la inicialización de ventanas de mi propia T2, y tomé una implementación de generador por chunks en `encoding.py` de [GeeksForGeeks](https://www.geeksforgeeks.org/break-list-chunks-size-n-python/).
