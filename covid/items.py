# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CovidItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    covidStats = scrapy.Field()
    news = scrapy.Field()
    getHelp = scrapy.Field()


class CovidSymptomsItem(scrapy.Item):
    title = scrapy.Field()
    symptoms = scrapy.Field()