# Tarea 2: DCCrossy Frog :school_satchel:


## Consideraciones generales :octocat:

En teoría está todo implementado, sin contar los bonus.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Ventana de Inicio: 4 pts (3%)
##### ✅ Ventana de Inicio
#### Ventana de Ranking: 5 pts (4%)
##### ✅ Ventana de Ranking
#### Ventana de juego: 13 pts (11%)
##### ✅ Ventana de juego
#### Ventana de post-nivel: 5 pts (4%)
##### ✅ Ventana post-nivel
#### Mecánicas de juego: 69 pts (58%)
##### ✅ Personaje
##### ✅ Mapa y Áreas de juego
##### ✅ Objetos
##### ✅ Fin de Nivel
##### ✅ Fin del juego
#### Cheatcodes: 8 pts (7%)
##### ✅ Pausa
##### ✅ V + I + D
##### ✅ N + I + V
#### General: 14 pts (12%)
##### ✅ Modularización
##### ✅ Modelación
##### ✅ Archivos
##### ✅ Parametros.py
#### Bonus: 10 décimas máximo
##### ❌ Ventana de Tienda
##### ❌ Música
##### ❌ Checkpoint

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. No se requiren otros archivos independientes a los módulos, los sprites y las ventanas (.ui) en `ventanas/`.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. \_\_future\_\_`: se utiliza para proveer type hints de colecciones en formato retrocompatible a 3.8. (`list[str]` en vez de `List[str]` importado de `typing`).
2. `typing`: se utiliza para crear objetos de tipo `NamedTuple` que mejoran la versión incluída en `collection`, permitiendo declarar sus tipos para facilitar análisis estático. También agrega hints como `Union` y `Optional`, para facilitar el tipado.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `state`: Regula la vasta mayoría del estado en el back-end, salvo por el spawneo en el caso del rio y la carretera. Controla transiciones y coordina la vasta mayoría de señales.
2. `games`: Implementa el front-end para la carretera y el río.
3. `froggy_and_objects`: Implementa el front-end para Froggy y los objetos especiales. Coordina colisiones.
4. `db`: Incluye funciones para la escritura y lectura de `puntajes.txt`.
5. `parameters`: Incluye los parámetros generales del juego.

## Supuestos y consideraciones adicionales :thinking:
1. En el río una opción adecuada es bloquear las teclas de adelante y atrás. Me hace sentido porque además transmite al usuario que debe usar la tecla espacio para desplazarse en ese segmento.
2. La mayoría de los tipos del programa están específicados utilizando type hints acorde con [PEP 484](https://www.python.org/dev/peps/pep-0484/) y [PEP 585](https://www.python.org/dev/peps/pep-0585/). Estos no afectan el flujo de ejecución del programa y solo ayudan al análisis estático del programa.
3. Las señales siguen la convención de ser creadas donde son emitidas, pero hay excepciones puntuales donde hay emisores múltiples. Intenté mantener la relación entre señales lo más limpia posible, pero no diré que está hermoso.
4. Mi criterio para dividir el back-end y el front-end fue delegar todo lo que tuviera que ver con pixeles, posiciones e imágenes hacia los `Views`, mientras que el back-end modela todas las transiciones de estado y parámetros necesarios para describir el juego abstractamente. En algunos casos, el front-end modifica directamente el estado en el back-end, por lo que usé properties extensamente para crear interfaces limpias.
5. Espero que las tipografías funcionen bien. Usé variaciones de Roboto en menús, y me aseguré que las stylesheets tuvieran un fallback de `sans-serif` pero desconozco la implementación de Qt al respecto, así que no sé si se va a ver bien.
6. Comenté todo en inglés de puro hábito, espero que igual se entienda todo bien uwu

-------

## Referencias de código externo :book:

No usé código externo, pero GitHub Copilot aportó con snippets generados de vez en cuando. (La mayoría variaciones del código ya existente)
