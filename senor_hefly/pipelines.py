# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from senor_hefly.models import Products, db_connect, create_products_table


class SenorHeflyPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_products_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        product = Products(**item)

        try:
            session.add(product)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

