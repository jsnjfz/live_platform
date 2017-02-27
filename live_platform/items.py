
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LivePlatformItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    platform_name = scrapy.Field()
    platform_type = scrapy.Field()
    platform_desc = scrapy.Field()
    channel_name = scrapy.Field()
    channel_type = scrapy.Field()
    channel_desc = scrapy.Field()
    room_id = scrapy.Field()
    name = scrapy.Field()
    watch_num = scrapy.Field()
    follow_num = scrapy.Field()
    url = scrapy.Field()
    room_desc = scrapy.Field()


