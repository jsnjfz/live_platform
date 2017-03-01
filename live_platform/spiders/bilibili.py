# -*- coding: utf-8 -*-
import scrapy

# 全部链接动态生成
class BooksSpider(scrapy.Spider):
    name = "quanmin"

    # allowed_domains = ['http://www.huajiao.com/']
    start_urls = ['https://www.quanmin.tv/game/lol']

    # def parse(self, response):
    #     # "//a[@target='_blank']/@href" 从category爬取用
    #     for href in response.xpath("//a[@class='g-trans p-category_card animated fadeInUp']/@href").extract():
    #         print "---" + href + "---"
    #         yield scrapy.Request(response.urljoin(href),
    #                              callback=self.parse_innerurl)

    # def parse_innerurl(self, response):
    #     for href in response.xpath("//*[@id='live-list-contentbox']/li/a/@href").extract():
    #         yield scrapy.Request(response.urljoin(href),
    #                              callback=self.parse_content)
    #
    #     next_page = response.xpath("//a[@class='w-paging_btn w-paging_ctrl w-paging_next false']/@href").extract_first()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse_innerurl)


    def parse(self, response):
        for href in response.xpath("//*[@id='live-list-contentbox']/li/a/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_content)

        next_page = response.xpath("//a[@class='w-paging_btn w-paging_ctrl w-paging_next false']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_content(self, response):
        # print "*******" + response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030') + "*******"
        title = response.xpath("//h1[@class='w-room-title_name']/text()").extract_first().strip()
        name = response.xpath("//span[@class='w-room-title_red']/text()").extract_first()
        # date = response.xpath("//*[@id='post-date']/text()").extract_first()
        watch_num = response.xpath("//span[@class='w-room-title_red js-online']/text()").extract_first()
        follow_num = response.xpath("//span[@class='w-room-title_favnum c-icon_favnum']/text()").extract_first()

        print "****title:****" + title
        print "****name:****" + name
        print "****watch_num:****" + watch_num
        print "****follow_num:****" + follow_num

        with open("quanmin", 'a+') as f:
            f.write("\n" + title + watch_num + follow_num + "\n")
        self.log('Saved file test')

        # page = response.url.split("/")[-1]
        # title = title.replace("/", "-").replace("?", "-").replace("?", "-").replace(":", "-").replace("*", "-").replace("<", "-").replace(">", "-").replace('"', '-')
        # filename = date + "-" + title + ".html"
        # with open(filename, 'wb') as f:
        #     f.write(response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030'))
        # self.log('Saved file %s' % filename)

