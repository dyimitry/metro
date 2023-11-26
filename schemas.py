from typing import Optional

from pydantic import BaseModel


class Region(BaseModel):
    id: int
    name: str


class Shop(BaseModel):
    merchant_id: int
    region_id: int
    adress: str


class Category(BaseModel):
    code: str
    count_products: int


class Product(BaseModel):
    region_id: int
    merchart_id: int
    sub_category_code: str
    product_id: int
    product_name: str
    product_brand: Optional[str] = None
    product_price: Optional[float] = None
    product_promo_price: Optional[float] = None
    product_url: Optional[str] = None
