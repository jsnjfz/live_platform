# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from ..items import LivePlatformItem

import json


class BilibiliSpider(Spider):
    name = 'bilibili'
    des = "b站"
    allowed_domains = ['bilibili.com']
    start_urls = [
        'http://live.bilibili.com/area/live'
    ]

    def parse(self, response):
        panel_class = ['live-top-nav-panel', 'live-top-hover-panel']
        panel_xpath = ['contains(@class, "{}")'.format(pclass) for pclass in panel_class]
        room_query_list = []
        for a_element in response.xpath('//div[{}]/a'.format(' and '.join(panel_xpath)))[1:]:
            div_list = a_element.xpath('div[@class="nav-item"]')
            if len(div_list) <= 0:
                continue
            div_element = div_list[0]
            url = a_element.xpath('@href').extract_first()
            short = url[url.rfind('/') + 1:]
            name = div_element.xpath('text()').extract_first()
            url = 'http://live.bilibili.com/area/liveList?area={}&order=online'.format(short)
            room_query_list.append({'url': url, 'channel': short, 'page': 1})
        for room_query in room_query_list:
            yield Request('{}&page=1'.format(room_query['url']), callback=self.parse_room_list, meta=room_query)


    def parse_room_list(self, response):
        room_list = json.loads(response.text)['data']
        if isinstance(room_list, list):
            for rjson in room_list:
                if isinstance(rjson['online'], int):
                    yield LivePlatformItem({
                        'platform_name': 'b站',
                        'platform_type': 'game',
                        'room_thumb': rjson['cover'],
                        'room_id': rjson['roomid'],
                        'channel_type': rjson['area'],
                        'channel_name': rjson['areaName'],
                        'follow_num': 999,
                        'watch_num': rjson['online'],
                        'name': rjson['uname'],
                        'room_desc': rjson['title'],
                        'url': response.urljoin(rjson['link']),
                        'room_status': rjson['is_tv'],
                    })
            if len(room_list) > 0:
                next_meta = dict(response.meta, page=response.meta['page'] + 1)
                yield Request('{}&page={}'.format(next_meta['url'], str(next_meta['page'])),
                              callback=self.parse_room_list, meta=next_meta)
