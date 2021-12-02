# -*- coding: utf-8 -*-
# http://sooyoung32.github.io/dev/2016/02/07/scrapy-tutorial.html
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Spider(scrapy.Spider):
    name = "textCrawler"

    def __init__(self):
        self.NUM_PAGE = 309
        self.start_urls = ['https://teen.munjang.or.kr/archives/category/write/life']

    def parse(self, response):
        url = self.start_urls[0]
        yield scrapy.Request(url, callback=self.parse_page)
        for n in range(1, self.NUM_PAGE+1):
            url = self.start_urls[0] + '/page/' + str(n)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        for post in response.css('[class=post_title] a::attr(href)').extract():
            yield scrapy.Request(post, callback=self.parse_text)

    def parse_text(self, post):
        dic = {}

        url = post.request.url.split('/')[-1]

        title = post.css('.entry-title::text').extract()
        dic['title'] = title[0]

        tokens = ['장원', '공지', '생활글', '월장원', '주장원', '이야기글', '알려드립니다', '필독', '[공지]', '작품', '글틴', '읽어보세요', '발표']
        for token in tokens:
            if token in title[0].split():
                return

        content = post.xpath('//*[@id="post-{}"]/div[1]/p//text()'.format(url)).extract()
        if not content:
            content = post.xpath('//*[@id="post-{}"]//div//text()'.format(url)).extract()

        content = " ".join(content)
        dic['content'] = self.PreProcess(content)

        yield dic

    def PreProcess(self, text):
      text = re.sub(pattern='Posted on [0-9]{4} [0-9]{2} [0-9]{2} .+ Posted in \S+ \s?', repl='', string=text)
      _filter = re.compile('[ㄱ-ㅣ]+')
      text = _filter.sub('', text)
      _filter = re.compile('[^가-힣 0-9 a-z A-Z \. \, \" \? \!]+')
      text = _filter.sub('', text)
      _filter = re.compile('[\n]+')
      text = _filter.sub("", text)
      return text
