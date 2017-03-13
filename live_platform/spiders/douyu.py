# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import LivePlatformItem


class BooksSpider(scrapy.Spider):
    name = "douyu"

    # allowed_domains = ['http://chuansong.me/']
    start_urls = ['https://www.douyu.com/directory']


    def parse(self, response):
        for href in response.xpath("//*[@id='live-list-contentbox']/li/a/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_innerurl)

        # nextPage = response.css('ul.pager li.next a::attr(href)').extract_first()
        # if nextPage:  # 如果找到下一页的url, 得到绝对路径, 构造新的Request对象.
        #     nextPage = response.urljoin(nextPage)
        #     yield scrapy.Request(nextPage, callback=self.parse)

        next_page = response.xpath("//a[@style='float: right']/@href").extract_first()
        print "****next_page****" + next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_innerurl(self, response):
        room_api = 'http://open.douyucdn.cn/api/RoomApi/room/'
        for href in response.xpath("//*[@id='live-list-contentbox']/li/a/@href").extract():
            yield scrapy.Request(room_api + href,
                                 callback=self.parse_content)



    def parse_content(self, response):
        item = LivePlatformItem()
        # 由于观众类型数据为动态生成，所以通过接口获取
        js = json.loads(response.body)

        if js['error'] != 0:
            print '调用接口失败: 返回错误结果'

        room_respjson = js['data']

        item['platform_name'] = '斗鱼TV'
        item['platform_type'] = 'game'
        item['room_thumb'] = room_respjson["room_thumb"]
        item['room_id'] = room_respjson["room_id"]
        item['channel_type'] = room_respjson["cate_id"]
        item['channel_name'] = room_respjson["cate_name"]
        item['follow_num'] = room_respjson["fans_num"]
        item['watch_num'] = room_respjson["online"]
        item['name'] = room_respjson["owner_name"]
        item['room_desc'] = room_respjson["room_name"]
        item['url'] = 'https://www.douyu.com/' + item['room_id']
        item['room_status'] = room_respjson["room_status"]

        # url = scrapy.Field()

        yield item

        # print "*******" + response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030') + "*******"
        # title = response.xpath("//*[@id='anchor-info']/div[2]/div[3]/ul/li[1]/div/a/text()").extract_first().encode('GB18030')
        # # date = response.xpath("//*[@id='post-date']/text()").extract_first()
        # watch_num = response.xpath("//a[@data-anchor-info='ol-num']/text()").extract_first()
        # follow_num = response.xpath("//span[@data-anchor-info='nic']/text()").extract_first()
        #
        # print "****title:****" + title
        # print "****watch_num:****" + watch_num
        # print "****follow_num:****" + follow_num
        #
        # follow_num = ""
        # watch_num = ""

        # with open("douyu", 'a+') as f:
        #     f.write( "****name:****" + name.encode('utf-8') + "****title:****" + title.encode('utf-8') + "****watch_num:****" + str(watch_num) + "****follow_num:****" + str(follow_num) + "\n")
        # self.log('Saved file test')

        # page = response.url.split("/")[-1]
        # title = title.replace("/", "-").replace("?", "-").replace("?", "-").replace(":", "-").replace("*", "-").replace("<", "-").replace(">", "-").replace('"', '-')
        # filename = date + "-" + title + ".html"
        # with open(filename, 'wb') as f:
        #     f.write(response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030'))
        # self.log('Saved file %s' % filename)

