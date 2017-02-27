# -*- coding: utf-8 -*-
import scrapy


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

        # next_page = response.xpath("//a[@style='float: right']/@href").extract_first()
        # print "****next_page****" + next_page
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_innerurl(self, response):
        for href in response.xpath("//*[@id='live-list-contentbox']/li/a/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_content)



    def parse_content(self, response):
        # print "*******" + response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030') + "*******"
        title = response.xpath("//*[@id='anchor-info']/div[2]/div[3]/ul/li[1]/div/a/text()").extract_first().encode('GB18030')
        # date = response.xpath("//*[@id='post-date']/text()").extract_first()
        watch_num = response.xpath("//a[@data-anchor-info='ol-num']/text()").extract_first()
        follow_num = response.xpath("//span[@data-anchor-info='nic']/text()").extract_first()

        print "****title:****" + title
        print "****watch_num:****" + watch_num
        print "****follow_num:****" + follow_num

        with open("test", 'a+') as f:
            f.write("\n" + title + watch_num + follow_num + "\n")
        self.log('Saved file test')

        # page = response.url.split("/")[-1]
        # title = title.replace("/", "-").replace("?", "-").replace("?", "-").replace(":", "-").replace("*", "-").replace("<", "-").replace(">", "-").replace('"', '-')
        # filename = date + "-" + title + ".html"
        # with open(filename, 'wb') as f:
        #     f.write(response.xpath("//div[@class='rich_media_content ']").extract_first().encode('GB18030'))
        # self.log('Saved file %s' % filename)

