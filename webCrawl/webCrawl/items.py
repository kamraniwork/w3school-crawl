# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TagItem(scrapy.Item):
    tag_name = scrapy.Field()
    tag_des = scrapy.Field()


class WebcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
