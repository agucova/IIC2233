# Tarea 0: DCCommerce :school_satchel:

## Consideraciones generales :octocat:
Todo debería funcionar bien, menos la remoción de comentarios junto con publicaciones. Corregí ese bug 1 minuto 9 segundos después de la entrega en el commit [`6c510ed`](https://github.com/IIC2233/agucova-iic2233-2021-2/commit/6c510edd1bd5b0b15d3010c86d9adf5a21407d80), no dándome cuenta que se entregaba a las 8:00 y no a las 8:30 :(

 Es un simple error de conversión de tipos de conversión entre un `str` con un `int`, y se puede utilizar el commit como referencia para arreglar la funcionalidad.

Todos los cambios posteriores eran cosméticos o de calidad, así que debería tener todo el resto de la funcionalidad ya implementada. Noté que dejé unos `TODO` en comentarios dando vuelta, pero todas esas mejoras ya están implementadas.

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
##### 🟠 Manejo de Archivos (Remoción de comentarios)
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
No utilicé código externo.
