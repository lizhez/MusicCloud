# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MusiccouldItem(scrapy.Item):

    table_name=scrapy.Field()
    table_fields=scrapy.Field()

    songid = scrapy.Field()
    title = scrapy.Field()
    singer = scrapy.Field()
    belong = scrapy.Field()
    contents = scrapy.Field()
    loadurl=scrapy.Field()
    
    pass
