from typing import List

import requests

from auchan.schemas import Shop

SHOPS_URL = "https://www.auchan.ru/v1/shops"


def list_shops(region_id: int) -> List[Shop]:
    shops: List[Shop] = []
    params = {"regionId": region_id}

    response = requests.get(SHOPS_URL, params=params)
    if response.status_code != 200:
        raise Exception("Запрос магазинов вернул ответ не с 200 статусом")

    json = response.json()
    response_shops = json["shops"]
    if response_shops is None:
        raise Exception("Магазины не найдены")

    for response_shop in response_shops:
        merchant_id = response_shop.get("merchant_id")
        region_id = response_shop.get("region_id")
        adress = response_shop.get("address_string")

        if merchant_id is None or region_id is None:
            continue

        magazine = Shop(
            merchant_id=merchant_id,
            region_id=region_id,
            adress=adress
        )
        shops.append(magazine)

    return shops
