from pokemon import (
    obtener_info_habilidad,
    obtener_pokemones,
    obtener_pokemon_mas_alto,
    obtener_pokemon_mas_rapido,
    obtener_mejores_atacantes,
    obtener_pokemones_por_tipo,
)
from api_curso import enviar_test, info_api_curso


token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2VtYWlsIjoiYWd1Y292YUB1Yy5jbCJ9.JGNkBO_9RcBRjsj8svTnSUEUOKf2904PeZEDs85kh7I"  # Ingresar tu API Token personal aquí

info_curso = info_api_curso(token)

if not info_curso:
    print("No se pudo obtener la información de la API del curso")
    exit()

url = info_curso["ability"]["url"]
info_habilidad = obtener_info_habilidad(url)
assert enviar_test(
    token, 1, info_habilidad
), "La función obtener_info_habilidad no retorna la información correcta"

pokemones = obtener_pokemones(info_habilidad["pokemon"])
assert enviar_test(
    token, 2, pokemones
), "La función obtener_pokemones no retorna la información correcta"

mas_alto = obtener_pokemon_mas_alto(pokemones)
assert enviar_test(
    token, 3, mas_alto
), "La función obtener_pokemon_mas_alto no retorna la información correcta"

mas_rapido = obtener_pokemon_mas_rapido(pokemones)
assert enviar_test(
    token, 4, mas_rapido
), "La función obtener_pokemon_mas_rapido no retorna la información correcta"

mejores_atacantes = obtener_mejores_atacantes(pokemones)
assert enviar_test(
    token, 5, mejores_atacantes
), "La función obtener_mejores_atacantes no retorna la información correcta"

pokemones_por_tipo = obtener_pokemones_por_tipo(pokemones)
assert enviar_test(
    token, 6, pokemones_por_tipo
), "La función obtener_pokemones_por_tipo no retorna la información correcta"

print("Mas alto", mas_alto)
print("Mas rapido", mas_rapido)
print("Mejores atacantes", mejores_atacantes)
print("Pokemones por tipo", pokemones_por_tipo)
