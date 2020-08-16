# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from scrapy.loader import ItemLoader
from senor_hefly.items import eGlupiItem


def current_time_date(self):
    now = datetime.now()
    dateString = now.strftime("%m/%d/%Y, %H:%M:%S")
    dataObject = datetime.strptime(dateString, "%m/%d/%Y, %H:%M:%S")
    return dataObject


class EglupiV2Spider(scrapy.Spider):
    name = "eGlupi_v2"
    start_urls = ["https://www.ekupi.hr/hr"]

    def parse(self, response):
        le = LinkExtractor(restrict_xpaths=["//ul[@class='sub-navigation-list has-title']/li[@class='yCmsComponent nav__link--secondary']/a | //ul[@class='sub-navigation-list ']/li[@class='yCmsComponent nav__link--secondary']/a"])
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_product)


    def parse_product(self, response):
        main_product_selector = "//div[@class='product-item']"
        product_link_selector = ".//a[@class='thumb']/@href"

        for product in response.xpath(main_product_selector):
            loader = ItemLoader(item=eGlupiItem(), selector=product)
            loader.add_value("date", current_time_date(self))
            loader.add_xpath("main_category_name", "//ol[@class='breadcrumb']/li[2]/a/text()")
            loader.add_xpath("sub_category_name", "//ol[@class='breadcrumb']/li[3]/a/text()")
            loader.add_xpath("sub_sub_category_name", "//ol[@class='breadcrumb']/li[@class='active']/text()")
            loader.add_xpath("main_product_link", ".//a[@class='thumb']/@href")
            loader.add_xpath("main_product_image", ".//a[@class='thumb']/img/@src")
            product_data = loader.load_item()

            product_url = product.xpath(product_link_selector).extract_first()
            yield response.follow(product_url, self.parse_product_detail, meta={"product_data": product_data}, dont_filter=True)

        le = LinkExtractor(restrict_xpaths=["//div[@class='pagination-bar top']/div[@class='pagination-toolbar']/div[@class='sort-refine-bar']/div[@class='row']/div[@class='col-xs-12 col-sm-6 col-md-5 pagination-wrap']/ul[@class='pagination']/li[@class='pagination-next']/a[@class='glyphicon glyphicon-chevron-right']"])
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_product)

    def parse_product_detail(self, response):
        product_data = response.meta["product_data"]
        product_detail_selector = "//div[@class='product-main-info']"

        # TODO: Ovo dolje, ubaciti u models i u pipeline, poseban pipeline i posebna tablica (one-to-one relationship)
        # table_rows = response.xpath("//table/tbody")
        # temp_product_data = dict()
        # temp_product_data["tableColumn1"] = table_rows.xpath("normalize-space(.//td[1]/text())").extract()
        # temp_product_data["tableColumn2"] = table_rows.xpath("normalize-space(.//td[2]/text())").extract()

        for product_detail in response.xpath(product_detail_selector):
            loader = ItemLoader(item=product_data, response=response, selector=product_detail)
            loader.add_xpath("main_product_name", ".//div[@class='product-details page-title hidden-xs hidden-sm']/div[@class='name']/text()")
            loader.add_xpath("main_product_price", ".//dd[@class='final-price']/text()")
            loader.add_xpath("main_product_price_old", ".//dd[@class='old-price']/text()")
            loader.add_xpath("main_product_warranty", ".//div[@class='info-hld']/p/b[contains(text(), 'Jamstvo:')]/text()")
            loader.add_xpath("main_product_payment_way", ".//div[@class='info-hld']/p[contains(text(), 'Platite')]/text()")
            loader.add_xpath("main_product_return", ".//div[@class='info-hld']/p[contains(text(), 'Povrat')]/text()")
            loader.add_xpath("main_product_delivery_date", ".//span[@class='ddate']/text()")
            # TODO: Ovo dolje
            # loader.add_value("main_product_table", dict(zip(temp_product_data["tableColumn1"], temp_product_data["tableColumn2"])))

            yield loader.load_item()
