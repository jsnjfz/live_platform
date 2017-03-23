# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from ..items import LivePlatformItem

import json


class BooksSpider(Spider):
    name = "zhanqi"
    des = "战旗TV"

    allowed_domains = ['zhanqi.tv']
    start_urls = [
        'https://www.zhanqi.tv/api/static/game.lists/300-1.json'
    ]

    def parse(self, response):
        room_query_list = []
        for cjson in json.loads(response.text)['data']['games']:
            url = 'https://www.zhanqi.tv/api/static/game.lives/{}/200-{{}}.json'.format(cjson['id'])
            room_query_list.append({'url': url, 'channel': cjson['gameKey'], 'page': 1})
        for room_query in room_query_list:
            yield Request(room_query['url'].format(str(room_query['page'])), callback=self.parse_room_list,
                          meta=room_query)

    def parse_room_list(self, response):
        room_list = json.loads(response.text)['data']['rooms']
        if isinstance(room_list, list):
            for rjson in room_list:
                yield LivePlatformItem({
                    'platform_name': '战旗TV',
                    'platform_type': 'game',
                    'room_thumb': rjson['spic'], # spic 小图,bpic 大图
                    'room_id': rjson['id'],
                    'channel_type': response.meta['channel'],
                    'channel_name': rjson['gameName'],
                    'follow_num': 999,
                    'watch_num': rjson['online'],
                    'name': rjson['nickname'],
                    'room_desc': rjson['title'],
                    'url': response.urljoin(rjson['url']),
                    'room_status': rjson['status'],
                })
            if len(room_list) > 0:
                next_meta = dict(response.meta, page=response.meta['page'] + 1)
                yield Request(next_meta['url'].format(str(next_meta['page'])), callback=self.parse_room_list,
                              meta=next_meta)
