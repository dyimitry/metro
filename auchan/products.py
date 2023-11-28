from typing import List, Any, Dict

import requests

from auchan.schemas import Product

PRODUCTS_URL = "https://www.auchan.ru/v1/catalog/products"
PRODUCTS_COUNT = 40


def list_products(region_id: int, merchant_id: int, sub_category_code: str, count_products: int) -> List[Product]:
    products: List[Product] = []

    params = {
        "merchantId": merchant_id,
        "page": 1,
        "perPage": PRODUCTS_COUNT
    }

    body = {
        "filter": {
            "category": sub_category_code,
            "promo_only": False,
            "active_only": False,
            "cashback_only": False
        }
    }

    count_pages = int(count_products / PRODUCTS_COUNT) + 1

    for page in range(1, count_pages + 1):
        params["page"] = page

        response = requests.get(PRODUCTS_URL, params=params, json=body)
        if response.status_code != 200:
            raise Exception("Запрос продуктов вернул ответ не с 200 статусом")

        json = response.json()
        response_products: List[Dict[str, Any]] = json.get("items")
        if response_products is None:
            raise Exception("Продкуты не найдены")

        for response_product in response_products:
            response_product_id = response_product.get("productId")
            response_product_title = response_product.get("title")
            if response_product_title is None or response_product_id is None:
                continue

            product = Product(
                region_id=region_id,
                merchart_id=merchant_id,
                sub_category_code=sub_category_code,
                product_id=response_product_id,
                product_name=response_product_title,
            )

            brand: Dict[str, Any] = response_product.get("brand")
            if brand is not None:
                brand_name = brand.get("name")
                if brand_name is not None:
                    product.product_brand = brand_name

            response_product_code = response_product.get("code")
            if response_product_code is not None:
                product.product_url = f"https://www.auchan.ru/product/{response_product_code}/"

            price: Dict[str, Any] = response_product.get("price")
            if price is not None:
                price_value = price.get("value")
                if price_value is not None:
                    product.product_price = price_value

            old_price: Dict[str, Any] = response_product.get("oldPrice")
            if old_price is not None:
                old_price_value = old_price.get("value")
                if old_price_value is not None:
                    product.product_promo_price = old_price_value

            products.append(product)

    return products
