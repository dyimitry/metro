from sqlalchemy.orm import Session

from auchan.schemas import Product
from db.db import Product


def product_add_in_db(session: Session, product: Product):
    tovar = Product(
        region_id=product.region_id,
        merchart_id=product.merchart_id,
        sub_category_code=product.sub_category_code,
        product_id=product.product_id,
        product_name=product.product_name,
        product_brand=product.product_brand,
        product_price=product.product_price,
        product_promo_price=product.product_promo_price,
        product_url=product.product_url,
    )
    session.add(tovar)
    session.commit()
