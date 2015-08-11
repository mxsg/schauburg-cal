# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieShowing(scrapy.Item):

    # general movie information
    name = scrapy.Field()
    # movieID = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    data = scrapy.Field()
    length = scrapy.Field()

    # information for a single movie showing
    dateTime = scrapy.Field()
    comment = scrapy.Field()

    def __repr__(self):
        return repr({"name": self["name"],
                "dateTime": self["dateTime"].isoformat()})
