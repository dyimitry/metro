from typing import List

import requests

from schemas import Region

REGION_NAME_MSC = "Москва и область"
REGION_NAME_SPB = "Санкт-Петербург и область"
REGION_URL = "https://www.auchan.ru/v1/regions"


def list_regions() -> List[Region]:
    list_reg: List[Region] = []
    response = requests.get(REGION_URL)
    if response.status_code != 200:
        raise Exception("Запрос регионов вернул ответ не с 200 статусом")

    json = response.json()
    regions = json.get("regions")
    if regions is None:
        raise Exception("Регионы не найдены")

    for region in regions:
        region_id = region.get("id")
        name = region.get("name")
        if name is None or region_id is None:
            continue

        if name == REGION_NAME_MSC:
            reg = Region(id=region_id, name=name)
            list_reg.append(reg)
            continue

        if name == REGION_NAME_SPB:
            reg = Region(id=region_id, name=name)
            list_reg.append(reg)

    return list_reg
