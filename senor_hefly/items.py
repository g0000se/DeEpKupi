from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime


def correct_price_format(text):
    text = text.replace(u'&nbsp kn', '').replace(u'.', '').replace(u',', '.')
    f = float(text)
    return f


def correct_warranty_format(text):
    text = text.replace(u'Jamstvo: ', '')
    return text


def correct_link_format(text):
    text = "https://www.ekupi.hr" + text
    return text


class eGlupiItem(Item):
    date = Field(output_processor=TakeFirst())
    main_product_name = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    main_category_name = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    sub_category_name = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    sub_sub_category_name = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    main_product_price = Field(input_processor=MapCompose(str.strip, correct_price_format), output_processor=TakeFirst())
    main_product_price_old = Field(input_processor=MapCompose(str.strip, correct_price_format), output_processor=TakeFirst())
    main_product_warranty = Field(input_processor=MapCompose(str.strip, correct_warranty_format), output_processor=TakeFirst())
    main_product_link = Field(input_processor=MapCompose(correct_link_format), output_processor=TakeFirst())
    main_product_image = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    main_product_payment_way = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    main_product_return = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    # main_product_table = Field()
    main_product_delivery_date = Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
