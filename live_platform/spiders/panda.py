# -*- coding: utf-8 -*-
import scrapy
import json

from live_platform.items import LivePlatformItem


class BooksSpider(scrapy.Spider):
    name = "panda"

    # CHANNEL_LIST_API = 'http://api.m.panda.tv/ajax_get_all_subcate'
    # ROOM_LIST_API = 'http://www.panda.tv/ajax_sort'
    # ROOM_API = 'http://www.panda.tv/api_room'

    # allowed_domains = ['http://www.huajiao.com/']
    start_urls = ['http://www.panda.tv/cate']

    def parse(self, response):
        for href in response.xpath("//a[@class='video-list-item-wrap']/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_innerurl)

    def parse_innerurl(self, response):
        room_api = 'http://www.panda.tv/api_room'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for href in response.xpath("//a[@class='video-list-item-wrap']/@href").extract():
            yield scrapy.Request(room_api + "?roomid=" + href[1:],
                                 callback=self.parse_content, headers=headers)

    def parse_content(self, response):
        item = LivePlatformItem()
        # 由于观众类型数据为动态生成，所以通过接口获取
        js = json.loads(response.body)

        if js['errno'] != 0:
            print '调用接口失败: 返回错误结果'

        respjson = js['data']

        host_respjson = respjson['hostinfo']
        room_respjson = respjson['roominfo']

        item['platform_name'] = '熊猫TV'
        item['platform_type'] = 'game'
        item['room_thumb'] = room_respjson["pictures"]["img"]
        item['room_id'] = room_respjson["id"]
        item['channel_type'] = room_respjson["cate"]
        item['channel_name'] = room_respjson["classification"]
        item['follow_num'] = room_respjson["fans"]
        item['watch_num'] = room_respjson["person_num"]
        item['name'] = host_respjson["name"]
        item['room_desc'] = room_respjson["name"]
        item['url'] = 'https://www.panda.tv/' + item['room_id']
        # 2在线
        item['room_status'] = room_respjson["status"]

        # url = scrapy.Field()

        yield item

