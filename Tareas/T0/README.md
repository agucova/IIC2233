# Tarea 0: DCCommerce :school_satchel:

## Consideraciones generales :octocat:

Creí que se entregaba a las 8:30, pero por suerte todos los cambios posteriores eran cosméticos o de pequeñas mejoras en el flujo de interacción, así que debería tener todo la funcionalidad ya implementada. Noté que dejé unos `TODO` en comentarios dando vuelta, pero todas esas mejoras ya están implementadas.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Menú de Inicio (14pts) (14%)
##### ✅ Requisitos
##### ✅ Iniciar sesión
##### ✅ Ingresar como usuario anónimo
##### ✅ Registrar usuario
##### ✅ Salir
#### Flujo del programa (35pts) (35%)
##### ✅ Menú Principal
##### ✅ Menú Publicaciones
##### ✅ Menú Publicaciones Realizadas
#### Entidades 15pts (15%)
##### ✅ Usuarios
##### ✅ Publicaciones
##### ✅ Comentarios
#### Archivos: 15 pts (15%)
##### ✅ Manejo de Archivos (Remoción de comentarios)
#### General: 21 pts (21%)
##### ✅ Menús
##### ✅ Parámetros
##### ✅ Módulos
##### ✅ PEP8

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main```.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. `typing` (librería estándar): Utilizado para facilitar type hints de colecciones, NamedTuples y otras estructuras.
2. `__future__` (librería estándar): `annotations`, permite usar anotaciones de type hints evaluadas de forma retrasada.
3. `dataclasses` (librería estándar): Utilizado para crear dataclasses, clases eficientes para contener datos estructurados.
4. `os` (librería estándar): Utilizado para operaciones en el sistema y detección de SO para tanto DB como prints con colores.
4. `colorama`: Facilita el uso de colores para el terminal (debe instalarse)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```model```: Contiene todas las entidades: `User`, `Price`, `Publication` y  `Comment`.
2. ```db```: Contiene funciones para todas las operaciones que involucren I/O a los CSV.
3. ```menu```: Incluye el código de todos los menús interactivos.
4. ```art```: Tiene el arte ASCII de DCComercio.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los precios pueden ser modelados (y escritos!) como floats y no solo ints. El sistema es resiliente y puede gestionar ambas formas de escribirlo en los CSVs, sin embargo se optó a favor de floats porque uno nunca sabe cuando DCComercio se podría volver un hit internacional y otras monedas lo necesitan!
2. Asumo que no hay ninguna clase de race conditions en el IO a los archivos. Me imagino que esta app se usa desde un solo terminal fijo, y no entre varios usuarios.
3. Asumo que los requisitos de usuarios no aplican retroactivamente.
4. Usé [colorama](https://pypi.org/project/colorama/) para las hacer portable el código de las negritas (`bold()`) y el `clear_screen()` también debería ser portable. Lamentablemente, no tenía como probarlo en Windows. Si por alguna razón no funciona, eliminaría los cuerpos de ambas funciones en `menu.py`.
5. Uso [type hints](https://realpython.com/lessons/type-hinting/) acorde con [PEP 448](https://www.python.org/dev/peps/pep-0484/) de forma externa en mi programa, por lo que se puede notar anotaciones de tipos adicionales en la definición de funciones, métodos y algunas variables. Éstas anotaciones no cambian la funcionalidad del programa y solo sirven para complementar herramientas de análisis estático como [Pyright](https://github.com/microsoft/pyright).

----

## Referencias de código externo :book:
- Para el método de remoción de líneas de código me orientó mucho [esta](https://stackoverflow.com/a/28057753) respuesta de StackOverflow pero la real inspiracion fue [este](https://stackoverflow.com/questions/4710067/how-to-delete-a-specific-line-in-a-file#comment97330530_28057753) comentario.
- Para el código de `clear_screen()` me basé en [este](https://www.geeksforgeeks.org/clear-screen-python/) artículo.
- [Copilot](https://copilot.github.com/) me ayudó con la secuencia ANSI de `bold()` y el formato de fechas con `datetime` (sigo sorprendido), pero no hizo ningún otro aporte sustancial.
