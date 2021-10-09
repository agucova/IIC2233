# Tarea X: Nombre de la tarea :school_satchel:

## Consideraciones generales :octocat:

En teoría, la tarea es una implementación completa.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos: 38 pts (27%)
##### ✅  Diagrama
##### ✅ Definición de clases, atributos y métodos
##### ✅ Relaciones entre clases
#### Simulaciones: 12 pts (8%)
##### ✅ Crear partida
#### Acciones: 43 pts (30%)
##### ✅ Tributo <explicacion\>
##### ✅ Objeto <explicacion\>
##### ✅ Ambiente <explicacion\>
##### ✅ Arena <explicacion\>
#### Consola: 34 pts (24%)
##### ✅ Menú inicio <explicacion\>
##### ✅ Menú principal <explicacion\>
##### ✅ Simular Hora <explicacion\>
##### ✅ Robustez <explicacion\>
#### Manejo de archivos: 15 pts (11%)
##### ✅ Archivos CSV  <explicacion\>
##### ✅ parametros.py <explicacion\>
#### Bonus: 3 décimas máximo
##### ❌ Guardar Partida <explicacion\>
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Se requiere de `{ambientes,arenas,objetos,tributos}.csv`.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```colorama```: Se utiliza la función ```init()``` para traducir automáticamente señales de negrita o limpieza de pantalla en Windows (debe instalarse).
2. ```dataclasses```: Se utiliza `@dataclass` para crear `Evento`.
3. `sys`: provee `exit()` para terminar la ejecución limpiamente.
4. `os`: permite correr `clear` o `cls` para limpiar la pantalla en menús de forma portable.
5. `__future__`: se utiliza para proveer type hints de colecciones en formato retrocompatible a 3.8. (`list[str]` en vez de `List[str]` importado de `typing`).
6. `typing`: se utiliza para crear objetos de tipo `NamedTuple` que faciliten la lectura de datos de CSV de forma genérica. El uso de `typing` permite declarar sus tipos para facilitar análisis estático.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `model.py`: Contiene la definición de todas las entidades, incluyendo `Arena`, `Tributo`, `Ambiente`, `Objeto`, y sus subclases.
2. `menus.py`: Contiene la definición de todas los menús y el flujo interactivo entre estos. Es dónde se concentra la lógica del programa.
3. `db.py`: Incluye las funciones de cargado de los archivos, instanciando los objetos necesarios de `model`. Toma buena parte de la T0.
4. `parameters.py`: Incluye los parámetros constantes del programa.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Todos los tipos del programa están específicados utilizando type hints acorde con [PEP 484](https://www.python.org/dev/peps/pep-0484/) y [PEP 585](https://www.python.org/dev/peps/pep-0585/). Estos no afectan el flujo de ejecución del programa y solo ayudan al análisis estático del programa.
2. Asumo que rendirse y salir son acciones equivalentes (ambos se mencionan en el enunciado, pero de forma aparentemente similar). Por eso, la acción para salir se implementa de forma genérica.


-------

## Referencias de código externo :book:

1. El código de limpieza de pantalla, negritas y menús abstractos implementado en `menus.py:10-65` proviene de mi tarea 0 al igual que el código abstracto para el cargado de CSVs genéricos en `db.py:23-39`.



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
