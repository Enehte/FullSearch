import pygame
import requests
import sys
import os
from geocoder import coordinates, get_coods_spn


def show_map(ll_spn, add_params=None):
    request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l=map"
    if add_params:
        request += "&" + add_params
    response = requests.get(request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as f:
            f.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    if toponym_to_find:
        lat, lon = coordinates(toponym_to_find)
        ll_spn = f"ll={lat},{lon}&spn=0.005,0.005"
        show_map(ll_spn)

        ll, spn = get_coods_spn(toponym_to_find)
        ll_spn = f"ll={ll}&spn={spn}"
        point_param = f"pt={ll}"
        show_map(ll_spn, add_params=point_param)
    else:
        print('No data')


if __name__ == "__main__":
    main()
