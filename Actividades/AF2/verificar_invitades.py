from __future__ import annotations
from invitades import Invitade


def verificar_edad(invitade: Invitade):
    assert isinstance(invitade.edad, int)
    if invitade.edad <= 0:
        raise ValueError(f"Error: la edad de {invitade.nombre} es negativa")


def corregir_edad(invitade: Invitade):
    assert isinstance(invitade.edad, int)
    try:
        verificar_edad(invitade)
    except ValueError as e:
        print(e)
        invitade.edad = abs(invitade.edad)
        print(f"El error en la edad de {invitade.nombre} ha sido corregido")


def verificar_pase_movilidad(invitade: Invitade):
    if not isinstance(invitade.pase_movilidad, bool):
        raise TypeError(
            f"Error: el pase de movilidad de {invitade.nombre} no es un bool"
        )


def corregir_pase_movilidad(invitade: Invitade):
    try:
        verificar_pase_movilidad(invitade)
    except TypeError as e:
        print(e)
        invitade.pase_movilidad = True
        print(f"Error: el pase de movilidad de {invitade.nombre} no es un bool")


def verificar_mail(invitade: Invitade):
    assert isinstance(invitade.mail, str)
    mail = invitade.mail.strip().split("@")
    assert len(mail) == 2
    if mail[0] == "uc" and mail[1] != "uc.cl":
        raise ValueError(
            f"Error: El mail de {invitade.nombre} no está en el formato correcto"
        )
    elif mail[1] != "uc.cl":
        print(
            f"Advertencia: El dominio de {invitade.nombre} no es uc.cl, sin embargo cumple la especificación."
        )


def corregir_mail(invitade: Invitade):
    assert isinstance(invitade.mail, str)
    try:
        verificar_mail(invitade)
    except ValueError as e:
        print(e)
        mail = invitade.mail.strip().split("@")
        assert len(mail) == 2
        assert mail[0] == "uc"

        dominio = mail[1].split(".")
        tld = dominio.pop()
        assert tld == "cl"
        usuario = ".".join(dominio)
        invitade.mail = f"{usuario}@uc.cl"
        print(f"El error en el mail de {invitade.nombre} ha sido corregido")


def dar_alerta_colado(
    nombre_asistente: str, diccionario_invitades: dict[str, Invitade]
):
    try:
        asistente = diccionario_invitades[nombre_asistente]
    except KeyError as e:
        print(e)
        print(f"Error: {nombre_asistente} se está intentando colar al carrete")
    else:
        print(f"{asistente.nombre} está en la lista y tiene edad {asistente.edad}")
