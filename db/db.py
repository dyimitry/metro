import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

session = Session(engine)


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer)
    merchart_id = Column(Integer)
    sub_category_code = Column(String(200))
    product_id = Column(Integer)
    product_name = Column(String(200))
    product_brand = Column(String(200))
    product_price = Column(Float)
    product_promo_price = Column(Float)
    product_url = Column(String(200))


Base.metadata.create_all(engine)
