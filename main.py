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
from auchan.schemas import Region, Shop, Category, CollectProduct


def parallel_collect_and_save_products(database_engine, collect_product):
    print(f"run thread: {threading.current_thread().name}")
    database_session = Session(database_engine)
    products = list_products(
        region_id=collect_product.region_id,
        merchant_id=collect_product.shop_merchant_id,
        sub_category_code=collect_product.category_code,
        count_products=collect_product.category_count_products
    )
    for product in products:
        product_add_in_db(database_session, product)
        file_writer.writerow(product.model_dump())


file = open("products.csv", mode="w", encoding='utf-8')

try:
    threads = []
    names = [
        "region_id", "merchart_id", "sub_category_code", "product_id",
        "product_name", "product_brand", "product_price", "product_promo_price", "product_url"
    ]
    file_writer = csv.DictWriter(file, delimiter=",", lineterminator="\r", fieldnames=names)
    file_writer.writeheader()

    regions: List[Region] = list_regions()

    id_tread = 1
    for region in regions:
        print(f"collect region {region.id}")

        shops: List[Shop] = list_shops(region.id)
        for shop in shops:
            print(f"collect shop {shop.merchant_id}")
            categories: List[Category] = list_categories(shop.merchant_id)
            for category in categories:
                print(f"collect category {category.code}")

                data_for_collect_products = CollectProduct(
                    region_id=region.id,
                    shop_merchant_id=shop.merchant_id,
                    category_code=category.code,
                    category_count_products=category.count_products
                )

                thread = threading.Thread(
                    name=f"thread_{id_tread}",
                    target=parallel_collect_and_save_products, args=(engine, data_for_collect_products,)
                )

                thread.start()

                id_tread += 1

                # for product in products:
                #     product_add_in_db(session, product)   #  НОВАЯ
                #     file_writer.writerow(product.model_dump())

    [t.join() for t in threads]
except Exception as e:
    print(e)
    file.close()



