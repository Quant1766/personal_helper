# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



from scrapy.item import Item, Field


class ProductItem(Item):
    person_slug = Field()
    rating =Field()
    name = Field()
    title = Field()
    webpage = Field()
    category = Field()
    subcategory =Field()
    description = Field()
    series = Field()
    manufactyrer = Field()
    photo = Field()
    organization = Field()
    size = Field()
    value = Field()
    currency = Field()
    prices = Field()
    characteristics = Field()
    chart_price = Field()
    shops = Field()
