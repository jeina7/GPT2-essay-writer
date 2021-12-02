# -*- coding: utf-8 -*-
# http://sooyoung32.github.io/dev/2016/02/07/scrapy-tutorial.html
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Spider(scrapy.Spider):
    name = "bookCrawler"

    def __init__(self):
        self.NUM_PAGE = 470
        self.start_urls = ['http://viewer.bookrail.co.kr/epub-viewer.do;jsessionid=28D800E3B07A56F919C1B88B7F84FAF9?page=1&systemCode=&documentId=11653&serviceName=bookrail']

    def parse(self, response):
        # url = self.start_urls[0]
        # yield scrapy.Request(url, callback=self.parse_page)
        # for n in range(1, self.NUM_PAGE+1):
        #     url = self.start_urls[0] + '/page/' + str(n)
        #     yield scrapy.Request(url, callback=self.parse_page)
        dic = {}

        # url = post.request.url.split('/')[-1]
        # dic['#'] = url
        url = self.start_urls[0]
        print(response.xpath('//p/text()'))

        # title = post.css('.entry-title::text').extract()
        # dic['title'] = title[0]

        # tokens = ['장원', '공지', '생활글', '월장원', '주장원', '이야기글', '알려드립니다', '필독', '[공지]', '작품', '글틴', '읽어보세요']
        # for token in tokens:
        #     if token in title[0].split():
        #         return

        # content = post.xpath('//*[@id="post-{}"]/div[1]/p//text()'.format(url)).re('(\w+)')
        # if not content:
        #     content = post.xpath('//*[@id="post-{}"]//div//text()'.format(url)).re('(\w+)')

        # content = " ".join(content)
        # dic['content'] = content

        # print(post)
        # print(title)
        # print(content)

        yield dic

    def parse_page(self, response):
        for post in response.css('[class=post_title] a::attr(href)').extract():
            yield scrapy.Request(post, callback=self.parse_text)

    def parse_text(self, post):
        dic = {}

        url = post.request.url.split('/')[-1]
        dic['#'] = url

        title = post.css('.entry-title::text').extract()
        dic['title'] = title[0]

        tokens = ['장원', '공지', '생활글', '월장원', '주장원', '이야기글', '알려드립니다', '필독', '[공지]', '작품', '글틴', '읽어보세요']
        for token in tokens:
            if token in title[0].split():
                return

        content = post.xpath('//*[@id="post-{}"]/div[1]/p//text()'.format(url)).re('(\w+)')
        if not content:
            content = post.xpath('//*[@id="post-{}"]//div//text()'.format(url)).re('(\w+)')

        content = " ".join(content)
        dic['content'] = content

        print(post)
        print(title)
        print(content)

        yield dic
