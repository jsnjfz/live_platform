# -*- coding: utf-8 -*-
import scrapy
from ..items import LivePlatformItem


class BooksSpider(scrapy.Spider):
    name = "huajiao"

    # allowed_domains = ['http://www.huajiao.com/']
    start_urls = ['http://www.huajiao.com/category/999', 'http://www.huajiao.com/category/666']

    # 栏目
    # 1001 音乐达人
    # 5 网络表演
    # 1 娱乐明星
    # 3 高清直播
    # 999 校园女生
    # 666 才艺直播
    # 2 女神驾到
    # 1000 热门推荐


    def parse(self, response):
        # "//a[@target='_blank']/@href" 从category爬取用
        for href in response.xpath("//div[@class='g-feed2']/a/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_content)

        next_page = response.xpath("//li[@class='paginate_button next']/a/@href").extract_first()
        # print "****next_page****" + next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_content(self, response):
        # print "*******" + response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030') + "*******"
        title = response.xpath("//*[@id='author-info']/div[1]/a/h3/text()").extract_first()
        # title = unicode(title, errors='ignore')
        # date = response.xpath("//*[@id='post-date']/text()").extract_first()
        watch_num = response.xpath("//*[@id='author-info']/div[5]/strong/text()").extract_first()
        follow_num = response.xpath("//*[@id='author-info']/div[3]/div[2]/h4/text()").extract_first()

        # title_u = u' '.join(title)
        print "****watch_num:****" + watch_num
        print "****follow_num:****" + follow_num

        item = LivePlatformItem()
        item['name'] = title.encode('utf-8')
        item['watch_num'] = watch_num.encode('utf-8')
        item['follow_num'] = follow_num.encode('utf-8')

        with open("test", 'a+') as f:
            f.write( "****title:****" + title.encode('utf-8') + "****watch_num:****" + watch_num.encode('utf-8') + "****follow_num:****" + follow_num.encode('utf-8') + "\n")

        # page = response.url.split("/")[-1]
        # title = title.replace("/", "-").replace("?", "-").replace("?", "-").replace(":", "-").replace("*", "-").replace("<", "-").replace(">", "-").replace('"', '-')
        # filename = date + "-" + title + ".html"
        # with open(filename, 'wb') as f:
        #     f.write(response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030'))
        # self.log('Saved file %s' % filename)

