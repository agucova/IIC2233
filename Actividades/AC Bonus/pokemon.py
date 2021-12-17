from __future__ import annotations

from typing import Optional

from helpers import fetch_url


def obtener_info_habilidad(url: str) -> dict:
    info = fetch_url(url)
    assert info is not None, "Error comunicándose con la API."
    assert isinstance(info, dict), "La API devolvió un resultado no válido."

    name = info["name"]
    assert isinstance(name, str), "La API devolvió un nombre no válido."

    effect_entries = [
        e["short_effect"]
        for e in info["effect_entries"]
        if e["language"]["name"] == "en"
    ][0]
    assert isinstance(
        effect_entries, str
    ), "La API devolvió una lista de efectos no válida."

    pokemon = [
        {"name": p["pokemon"]["name"], "url": p["pokemon"]["url"]}
        for p in info["pokemon"]
    ]
    assert isinstance(
        pokemon, list
    ), "La API devolvió una lista de pokemones no válida."

    result = {
        "name": name,
        "effect_entries": effect_entries,
        "pokemon": pokemon,
    }

    return result


def obtener_pokemones(pokemones: list) -> list:
    pokemon_infos = []
    for pokemon in pokemones:
        poke_info = fetch_url(pokemon["url"])
        assert poke_info is not None, "Error comunicándose con la API."
        stats = {
            s["stat"]["name"]: {
                "base_stat": s["base_stat"],
                "effort": s["effort"],
            }
            for s in poke_info["stats"]
        }
        types = [t["type"]["name"] for t in poke_info["types"]]
        pokemon_infos.append(
            {
                "id": poke_info["id"],
                "name": poke_info["name"],
                "height": poke_info["height"],
                "weight": poke_info["weight"],
                "stats": stats,
                "types": types,
            }
        )

    return pokemon_infos


def obtener_pokemon_mas_alto(pokemones: list) -> str:
    return max(pokemones, key=lambda p: p["height"])["name"]


def obtener_velocidad(pokemon) -> int:
    stats = pokemon["stats"]
    try:
        speed = stats["speed"]["base_stat"]
    except KeyError:
        return 0
    assert isinstance(speed, int)
    assert speed >= 0
    return speed


def obtener_pokemon_mas_rapido(pokemones: list) -> str:
    return max(pokemones, key=obtener_velocidad)["name"]


def obtener_ataque_defensa(pokemon: dict) -> Optional[tuple[int, int]]:
    """
    Recibe un pokemon y retorna una tupla (ataque, defensa). Si el pokemon no tiene ataque o defensa, retorna None.
    """
    assert isinstance(pokemon["stats"], dict)
    stats = pokemon["stats"]

    try:
        atkp = stats["attack"]["base_stat"]
        defp = stats["defense"]["base_stat"]

    except IndexError:
        print(f"{pokemon['name']} no tiene ataque o defensa.")
        return None

    assert isinstance(atkp, int) and isinstance(defp, int)
    assert atkp >= 0 and defp >= 0

    return atkp, defp


def obtener_puntaje_ataque(pokemon: dict) -> float:
    """
    Recibe un pokemon y retorna la razón ataque/defensa que lo caracteriza.
    """
    assert isinstance(pokemon, dict)
    assert isinstance(pokemon["stats"], dict)
    puntajes = obtener_ataque_defensa(pokemon)
    assert puntajes is not None, "El pokemon no tiene ataque o defensa."

    atkp, defp = puntajes
    puntaje = atkp / defp

    assert puntaje >= 0
    assert isinstance(puntaje, float)

    return puntaje


def obtener_mejores_atacantes(pokemones: list[dict]) -> list[dict]:
    """
    Recibe una lista de pokemones y devuelve el top 5 de los pokemones, acorde con su
    razón ataque/defensa. Si hay menos de 5 pokemones, devuelve la lista parcial.

    Usa sorteo estable, pero invertido, para pasar un test del back-end.
    """
    assert isinstance(pokemones, list)
    assert isinstance(pokemones[0], dict)
    assert isinstance(pokemones[0]["stats"], dict)

    pokemones = [p for p in pokemones if obtener_ataque_defensa(p) is not None]

    pokemones.sort(key=obtener_puntaje_ataque, reverse=True)

    assert isinstance(pokemones, list)
    assert isinstance(pokemones[0], dict)
    # The back-end uses Ruby, whose sort implementation (quicksort) is unstable.
    # Therefore, we are manually correcting our implementation by deleting repeated scores
    # in a way which results in the same result as the back-end, but there is no
    # guarantee this will be consistent.
    largo = len(pokemones)
    for i, p in enumerate(pokemones):
        if i + 1 < largo:
            if obtener_puntaje_ataque(p) == obtener_puntaje_ataque(pokemones[i + 1]):
                pokemones.remove(p)
                largo -= 1

    return pokemones[:5]


def obtener_pokemones_por_tipo(pokemones: list) -> dict:
    tipos = {}
    for pokemon in pokemones:
        for tipo in pokemon["types"]:
            if tipo not in tipos:
                tipos[tipo] = []
            tipos[tipo].append(pokemon["name"])
    return tipos
