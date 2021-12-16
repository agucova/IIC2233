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
    return sum([stats[s]["base_stat"] for s in stats if s == "speed"])


def obtener_ataque_defensa(pokemon: dict) -> Optional[tuple[int, int]]:
    stats = pokemon["stats"]

    try:
        atkp = [stats[s]["base_stat"] for s in stats if s == "attack"][0]
        defp = [stats[s]["base_stat"] for s in stats if s == "defense"][0]
    except IndexError:
        return None

    return atkp, defp


def obtener_puntaje_ataque(pokemon: dict) -> float:
    puntajes = obtener_ataque_defensa(pokemon)
    assert puntajes is not None, "El pokemon no tiene ataque ni defensa."
    atkp, defp = puntajes
    return atkp / defp


def obtener_pokemon_mas_rapido(pokemones: list) -> str:
    return max(pokemones, key=obtener_velocidad)["name"]


def obtener_mejores_atacantes(pokemones: list[dict]) -> list:
    to_sort = []
    for pokemon in pokemones:
        puntajes = obtener_ataque_defensa(pokemon)
        if puntajes is None:
            continue

        to_sort.append(pokemon)

    sorted_pokemones = sorted(to_sort, key=obtener_puntaje_ataque, reverse=True)
    if len(sorted_pokemones) < 5:
        return sorted_pokemones
    return sorted_pokemones[:5]


def obtener_pokemones_por_tipo(pokemones: list) -> dict:
    tipos = {}
    for pokemon in pokemones:
        for tipo in pokemon["types"]:
            if tipo not in tipos:
                tipos[tipo] = []
            tipos[tipo].append(pokemon["name"])
    return tipos
