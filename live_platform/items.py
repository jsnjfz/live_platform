
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LivePlatformItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    platform_name = Field()
    platform_type = Field()
    platform_desc = Field()
    channel_name = Field()
    channel_type = Field()
    channel_desc = Field()
    room_id = Field()
    name = Field()
    watch_num = Field()
    follow_num = Field()
    url = Field()
    room_desc = Field()
    room_thumb = Field()
    room_status = Field()


class ChannelItem(Item):
    office_id = Field()
    short = Field()
    name = Field()
    image = Field()
    url = Field()


