from typing import List, Optional
import csv
from auchan.regions import list_regions
from auchan.shops import list_shops
from auchan.categories import list_categories
from auchan.products import list_products

from schemas import Region, Shop, Category

file = open("products.csv", mode="w", encoding='utf-8')

try:
    names = [
        "region_id", "merchart_id", "sub_category_code", "product_id",
        "product_name", "product_brand", "product_price", "product_promo_price", "product_url"
    ]
    file_writer = csv.DictWriter(file, delimiter=",", lineterminator="\r", fieldnames=names)
    file_writer.writeheader()

    regions: List[Region] = list_regions()

    for region in regions:
        print(f"collect region {region.id}")

        shops: List[Shop] = list_shops(region.id)
        for shop in shops:
            print(f"collect shop {shop.merchant_id}")
            categories: List[Category] = list_categories(shop.merchant_id)
            for category in categories:
                print(f"collect category {category.code}")
                products = list_products(region.id, shop.merchant_id, category.code, category.count_products)
                for product in products:
                    file_writer.writerow(product.model_dump())

except Exception as e:
    print(e)
    file.close()

