import scrapy


class SpencersavingsItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
