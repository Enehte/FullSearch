import requests


def geocode(top):
    request = f"http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": top,
        "format": "json"}
    response = requests.get(request, params=params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {request}
            Http статус: {response.status_code} ({response.reason})""")
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]


def coordinates(top):
    toponym = geocode(top)
    if not toponym:
        return None, None
    coodrinates = toponym["Point"]["pos"]
    toponym_long, toponym_lat = coodrinates.split(" ")
    return float(toponym_long), float(toponym_lat)


def get_coods_spn(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)

    coodrinates = toponym["Point"]["pos"]
    toponym_long, toponym_lat = coodrinates.split(" ")
    ll = f'{toponym_long},{toponym_lat}'
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    spn = f"{dx},{dy}"
    return ll, spn