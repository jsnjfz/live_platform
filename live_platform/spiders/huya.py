# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from ..items import LivePlatformItem

import json


class BooksSpider(Spider):
    name = "huya"
    des = "虎牙TV"

    allowed_domains = ['huya.com']
    start_urls = [
        'http://www.huya.com/g'
    ]

    def parse(self, response):
        room_query_list = []
        for a_element in response.xpath('//li[@class="game-list-item"]/a'):
            url = a_element.xpath('@href').extract_first()
            short = url[url.rfind('/') + 1:]
            report_attr = json.loads(a_element.xpath('@report').extract_first())
            office_id = report_attr['game_id']
            img_element = a_element.xpath('img')[0]
            name = img_element.xpath('@title').extract_first()
            image = img_element.xpath('@data-original').extract_first()
            url = 'http://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&tagAll=0&gameId={}'.format(office_id)
            room_query_list.append({'url': url, 'channel': short, 'page': 1})
        for room_query in room_query_list:
            yield Request('{}&page=1'.format(room_query['url']), callback=self.parse_room_list, meta=room_query)

    def parse_room_list(self, response):
        room_list = json.loads(response.text)['data']['datas']
        if isinstance(room_list, list):
            for rjson in room_list:
                yield LivePlatformItem({
                    'platform_name': '虎牙TV',
                    'platform_type': 'game',
                    'room_thumb': rjson['screenshot'],
                    'room_id': rjson['uid'],
                    'channel_type': rjson['gameHostName'],
                    'channel_name': rjson['gameFullName'],
                    'follow_num': 999,
                    'watch_num': rjson['totalCount'],
                    'name': rjson['nick'],
                    'room_desc': rjson['roomName'],
                    'url': response.urljoin(rjson['privateHost']),
                    'room_status': rjson['liveSourceType'],
                })
            if len(room_list) > 0:
                next_meta = dict(response.meta, page=response.meta['page'] + 1)
                yield Request('{}&page={}'.format(next_meta['url'], str(next_meta['page'])),
                              callback=self.parse_room_list, meta=next_meta)
