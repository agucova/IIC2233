```mermaid
classDiagram
    Objeto <|-- Consumible
    Objeto <|-- Arma
    Objeto <|-- Especial
    Ambiente <|-- Bosque
    Ambiente <|-- Montana
    Ambiente <|-- Playa

    Arena o-- "3" Ambiente : sostiene
    Ambiente o-- "3" Evento : posee
    Arena o-- Tributo : juega
    Tributo *-- "0..*" Objeto : en mochila

    <<abstract>> Ambiente
    <<abstract>> Objeto
    class Arena {
        +str nombre
        +str dificultad
        +float riesgo
        +list~Ambiente~ ambientes
        +Ambiente ambiente
        +Ambiente proximo_ambiente
        +list~Jugador~ jugadores

        -int i_ambiente
        -int jugadores_cargados

        cargar_jugadores(Tributo jugador, list~Tributo~ tributos)
        mostrar_estado()
        siguiente_ambiente()
        ejecutar_evento()
        realizar_encuentros()
    }

    class Ambiente {
        +str nombre
        +list~Evento~ eventos
        calcular_dano(Evento evento)
    }

    Bosque : calcular_dano(Evento evento)
    Montana : calcular_dano(Evento evento)
    Playa : calcular_dano(Evento evento)

    class Evento {
        +str nombre
        +int dano
    }


    class Tributo {
        +str nombre
        +str distrito
        +int edad
        +int vida
        +int energia
        +int agilidad
        +int fuerza
        +int popularidad
        +bool esta_vive
        +list~Objeto~ mochila
        -int vida_

        mostrar_estado()

        atacar(Tributo tributo, bool es_encuentro)
        accion_heroica()
        hacerse_bolita()

        pedir_objeto(list~Objeto~ objetos)
        utilizar_objeto(Objeto objeto, Arena arena)
    }

    class Objeto {
        +str nombre
        +int peso

        entregar_beneficio(Tributo tributo, Arena arena)
    }

    Consumible : entregar_beneficio(Tributo tributo, Arena arena)
    Consumible : +str tipo
    Arma : entregar_beneficio(Tributo tributo, Arena arena)
    Arma : +str tipo
    Especial : entregar_beneficio(Tributo tributo, Arena arena)
    Especial : +str tipo
```
