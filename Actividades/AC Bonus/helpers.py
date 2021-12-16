import requests


def fetch_url(url, params=None, headers=None):
    if not headers:
        headers = {}
    if not params:
        params = {}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200 or not isinstance(result := response.json(), dict):
        return None
    return result


def fetch_endpoint(base_url: str, endpoint: str, params=None, headers=None):
    """
    Fetch an endpoint from the API.
    """

    assert base_url[-1] == "/", "Base URL must end with a slash"
    assert endpoint[0] != "/", "Endpoint must not start with a slash"

    url = base_url + endpoint
    return fetch_url(url, params, headers)


def post_endpoint(base_url: str, endpoint: str, data=None, params=None, headers=None):
    """
    Fetch an endpoint from the API.
    """
    if not headers:
        headers = {}
    if not params:
        params = {}
    if not data:
        data = {}

    assert base_url[-1] == "/", "Base URL must end with a slash"
    assert endpoint[0] != "/", "Endpoint must not start with a slash"

    url = base_url + endpoint
    response = requests.post(url, json=data, params=params, headers=headers)
    if response.status_code != 200 or not isinstance(result := response.json(), dict):
        return None

    return result


AVANZADA_API_BASE_URL = "https://www.avanzada.ml/api/v2/bonus/"


def fetch_api_cursos(endpoint, params=None, headers=None):
    return fetch_endpoint(AVANZADA_API_BASE_URL, endpoint, params, headers)


def post_api_cursos(endpoint, data=None, params=None, headers=None):
    return post_endpoint(AVANZADA_API_BASE_URL, endpoint, data, params, headers)
