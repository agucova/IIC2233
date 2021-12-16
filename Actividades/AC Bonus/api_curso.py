from typing import Any, Optional

from helpers import fetch_api_cursos, post_api_cursos


def info_api_curso(token: str) -> Optional[dict]:
    assert isinstance(token, str)
    return fetch_api_cursos("ability/", params={"api_token": token})


TEST_NAMES = {
    1: "obtener_info_habilidad",
    2: "obtener_pokemones",
    3: "obtener_pokemon_mas_alto",
    4: "obtener_pokemon_mas_rapido",
    5: "obtener_mejores_atacantes",
    6: "obtener_pokemones_por_tipo",
}


def enviar_test(token: str, test_id: int, respuesta: Any) -> bool:
    data = {
        "test": {
            "function_name": TEST_NAMES[test_id],
            "function_response": respuesta,
        }
    }
    print(data)
    test = post_api_cursos(f"tests/{test_id}", params={"api_token": token}, data=data)

    if not test:
        print(f"No se pudo enviar el test {test_id}")
        return False

    if test["result"] == "success":
        return True
    else:
        print(f"Error en el test {test_id}: {test['message']}")
        return False
