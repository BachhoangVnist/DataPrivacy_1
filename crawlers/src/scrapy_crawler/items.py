# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QACrawlerItem(scrapy.Item):

    question = scrapy.Field()
    answer = scrapy.Field()
    original_url = scrapy.Field()
