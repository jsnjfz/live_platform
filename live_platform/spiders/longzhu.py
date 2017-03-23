# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from ..items import LivePlatformItem

import json


class LongZhuSpider(Spider):
    name = 'longzhu'
    des = "龙珠TV"
    allowed_domains = ['longzhu.com', 'plu.cn']
    start_urls = [
        'http://www.longzhu.com/channels'
    ]

    def parse(self, response):
        channel_list = {}
        for div_element in response.xpath('//div[@class="list-item-thumb"]'):
            a_element = div_element.xpath('a')[0]
            url = a_element.xpath('@href').extract_first()
            short = url[url.rfind('/') + 1:]
            name = a_element.xpath('@title').extract_first()
            image = a_element.xpath('img/@src').extract_first()
            channel_list[short] = {
                'short': short,
                'name': name,
                'image': image,
                'url': response.urljoin(url),
                'sent': False
            }
        room_query = {
            'url': 'http://api.plu.cn/tga/streams?max-results=50&sort-by=top',
            'offset': 0, 'channels': channel_list
        }
        yield Request('{}&start-index=0'.format(room_query['url']), callback=self.parse_room_list, meta=room_query)

    def parse_room_list(self, response):
        channel_list = response.meta['channels']
        room_list = json.loads(response.text)['data']['items']
        if isinstance(room_list, list):
            for mixjson in room_list:
                cjson = mixjson['game'][0]
                if not cjson['tag']:
                    continue
                # if cjson['tag'] in channel_list:
                #     if not channel_list[cjson['tag']]['sent']:
                #         channel_list[cjson['tag']]['sent'] = True
                #         yield ChannelItem({
                #             'office_id': str(cjson['id']),
                #             'short': channel_list[cjson['tag']]['short'],
                #             'name': channel_list[cjson['tag']]['name'],
                #             'image': channel_list[cjson['tag']]['image'],
                #             'url': channel_list[cjson['tag']]['url']
                #         })
                # else:
                #     yield ChannelItem({
                #         'office_id': str(cjson['id']),
                #         'short': cjson['tag'],
                #         'name': cjson['name'],
                #         'url': 'http://www.longzhu.com/channels/' + cjson['tag']
                #     })
                rjson = mixjson['channel']

                yield LivePlatformItem({
                    'platform_name': '龙珠TV',
                    'platform_type': 'game',
                    'room_thumb': mixjson['preview'],
                    'room_id': rjson['id'],
                    'channel_type': cjson['tag'],
                    'channel_name': cjson['name'],
                    'follow_num': rjson['followers'],
                    'watch_num': mixjson['viewers'],
                    'name': rjson['name'],
                    'room_desc': rjson['status'],
                    'url': rjson['url'],
                    'room_status': rjson['_type'],
                })
            if len(room_list) > 0:
                next_meta = response.meta
                next_meta['offset'] += 50
                yield Request('{}&start-index={}'.format(next_meta['url'], str(next_meta['offset'])),
                              callback=self.parse_room_list, meta=next_meta)
