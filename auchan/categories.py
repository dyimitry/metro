from typing import List

import requests

from schemas import Category

CATEGORIES_URL = "https://www.auchan.ru/v1/categories"
BASE_CATEGORY_CODE = "syry"


def list_categories(merchant_id: int) -> List[Category]:
    params = {"merchant_id": merchant_id}
    response = requests.get(CATEGORIES_URL, params=params)
    if response.status_code != 200:
        raise Exception("Запрос категорий вернул ответ не с 200 статусом")

    categories: List[Category] = []

    response_categories = response.json()
    for response_category in response_categories:
        if response_category.get("code") == BASE_CATEGORY_CODE:
            if response_category.get("items") is not None:
                for response_sub_category in response_category.get("items"):
                    code = response_sub_category.get("code")
                    count_products = response_sub_category.get("productsCount")
                    if code is not None:
                        categories.append(
                            Category(
                                code=code,
                                count_products=count_products
                            )
                        )
    return categories
