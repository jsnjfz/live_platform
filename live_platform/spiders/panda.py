# -*- coding: utf-8 -*-
import scrapy

class BooksSpider(scrapy.Spider):
    name = "panda"

    # CHANNEL_LIST_API = 'http://api.m.panda.tv/ajax_get_all_subcate'
    # ROOM_LIST_API = 'http://www.panda.tv/ajax_sort'
    # ROOM_API = 'http://www.panda.tv/api_room'

    # allowed_domains = ['http://www.huajiao.com/']
    start_urls = ['http://www.panda.tv/cate']

    def parse(self, response):
        for href in response.xpath("//a[@class='video-list-item-wrap']/@href").extract():
            print "---" + href + "---"
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_innerurl)

    def parse_innerurl(self, response):
        for href in response.xpath("//a[@class='video-list-item-wrap']/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_content)

    def parse_content(self, response):
        # print "*******" + response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030') + "*******"
        # title = response.xpath("//h1[@class='room-head-info-title']/text()").extract_first().strip('\n')
        name = response.xpath("//span[@class='room-head-info-hostname']/text()").extract_first()
        # date = response.xpath("//*[@id='post-date']/text()").extract_first()
        watch_num = response.xpath("//div[@class='room-viewer-num']/span[1]/text()").extract_first()
        follow_num = response.xpath("//span[@class='w-room-title_favnum c-icon_favnum']/text()").extract_first()

        # print "****title:****" + title
        print "****name:****" + name
        print "****watch_num:****" + watch_num
        print "****follow_num:****" + follow_num

        with open("xiongmao", 'a+') as f:
            f.write("\n" + name + watch_num + follow_num + "\n")
        self.log('Saved file test')

        # page = response.url.split("/")[-1]
        # title = title.replace("/", "-").replace("?", "-").replace("?", "-").replace(":", "-").replace("*", "-").replace("<", "-").replace(">", "-").replace('"', '-')
        # filename = date + "-" + title + ".html"
        # with open(filename, 'wb') as f:
        #     f.write(response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030'))
        # self.log('Saved file %s' % filename)

