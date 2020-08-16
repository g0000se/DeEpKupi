from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from senor_hefly import settings

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_products_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Products(DeclarativeBase):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    date = Column("date", DateTime, nullable=True)
    main_category_name = Column("main_category_name", String, nullable=True)
    sub_category_name = Column("sub_category_name", String, nullable=True)
    sub_sub_category_name = Column("sub_sub_category_name", String, nullable=True)
    main_product_link = Column("main_product_link", String, nullable=True)
    main_product_image = Column("main_product_image", String, nullable=True)
    main_product_name = Column("main_product_name", String, nullable=True)
    main_product_warranty = Column("main_product_warranty", String, nullable=True)
    main_product_payment_way = Column("main_product_payment_way", String, nullable=True)
    main_product_return = Column("main_product_return", String, nullable=True)
    main_product_delivery_date = Column("main_product_delivery_date", String, nullable=True)
    main_product_price = Column("main_product_price", Float, nullable=True)
    main_product_price_old = Column("main_product_price_old", Float, nullable=True)

# TODO: nadodati novu tablicu "attributes". Svaki produkt može imati dodatne atribute, npr. Brand, Broj jezgri, Kamera, itd.