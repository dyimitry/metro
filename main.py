import threading
from typing import List
import csv

from sqlalchemy.orm import Session

from auchan.regions import list_regions
from auchan.shops import list_shops
from auchan.categories import list_categories
from auchan.products import list_products
from db.db import engine
from db.add_product import product_add_in_db
from auchan.schemas import Region, Shop, Category, CollectCategories


def parallel_collect_and_save(database_engine, collect_category):
    print(f"run thread: {threading.current_thread().name}")
    database_session = Session(database_engine)

    for category in collect_category.categories:
        print(f"collect category {category.code}")
        products = list_products(
            region_id=collect_category.region_id,
            merchant_id=collect_category.shop_merchant_id,

            sub_category_code=category.code,
            count_products=category.count_products
        )
        for product in products:
            product_add_in_db(database_session, product)

try:
    threads = []

    regions: List[Region] = list_regions()

    id_tread = 1

    for region in regions:
        print(f"collect region {region.id}")

        shops: List[Shop] = list_shops(region.id)
        for shop in shops:
            print(f"collect shop {shop.merchant_id}")
            categories: List[Category] = list_categories(shop.merchant_id)

            data_for_collect_categories = CollectCategories(
                region_id=region.id,
                shop_merchant_id=shop.merchant_id,
                categories=categories
            )

            thread = threading.Thread(
                name=f"thread_{id_tread}",
                target=parallel_collect_and_save, args=(engine, data_for_collect_categories,)
            )

            thread.start()

            id_tread += 1

    [t.join() for t in threads]
    # после завершения всех потоков можно считывать данные из бд и писать в файл если необходимо

except Exception as e:
    print(e)



