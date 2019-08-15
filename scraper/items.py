# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SuperProfItem(scrapy.Item):
    website = scrapy.Field()
    url = scrapy.Field()
    index = scrapy.Field() 
    search_topic = scrapy.Field()
    search_location = scrapy.Field()
    teacher = scrapy.Field()
    picture = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    ambassador = scrapy.Field()
    first_free = scrapy.Field()
