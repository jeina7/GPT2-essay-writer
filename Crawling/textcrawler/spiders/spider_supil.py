# -*- coding: utf-8 -*-
# http://sooyoung32.github.io/dev/2016/02/07/scrapy-tutorial.html
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class Spider(scrapy.Spider):
    name = "supilCrawler"

    def __init__(self):
        self.NUM_PAGE = 470
        self.start_urls = ['http://www.supil.or.kr/essay/talkpart/list.html?partid=10&code=talk2&page=1&part_name=%B5%BF%C0%CE%C1%F6%BC%D2%B0%B3&keyfield=&key=']
        self.url = 'http://www.supil.or.kr/essay'
        self.url_talkbox = 'http://www.supil.or.kr/essay/talkbox/'
        
    def parse(self, response):
        url = self.start_urls[0]
        yield scrapy.Request(url, callback=self.parse_page)
        for n in range(2, 5):
          if n == 2:
            url = 'http://www.supil.or.kr/essay/talkpart/list.html?partid=58&code=talk2&page='+str(n)+'&part_name=%B5%BF%C0%CE%C1%F6%BC%D2%B0%B3&keyfield=&key='
          if n == 3:  
            url = 'http://www.supil.or.kr/essay/talkpart/list.html?partid=27&code=talk2&page='+str(n)+'&part_name=%B5%BF%C0%CE%C1%F6%BC%D2%B0%B3&keyfield=&key='
          if n == 4:  
            url = 'http://www.supil.or.kr/essay/talkpart/list.html?partid=17&code=talk2&page='+str(n)+'&part_name=%B5%BF%C0%CE%C1%F6%BC%D2%B0%B3&keyfield=&key='
          yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        for post in response.css('[class=sbody] a::attr(href)').extract():
            # tmp = post[2:]
            # print(tmp)
            yield scrapy.Request(self.url + post[2:], callback=self.parse_list)

    def parse_list(self, response):
        for post in response.css('[class=sbody] a::attr(href)').extract():
            yield scrapy.Request(self.url_talkbox+post, callback=self.parse_text)

    def parse_text(self, post):
        dic = {}

        # url = post.request.url.split('/')[-1]
        # dic['#'] = url

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
        title = post.xpath('//b/text()').extract()
        title = title[0]
        # content = post.css('tbody::text').extract()
        content = post.xpath('//font/text()').extract()#.re('(\w+)')
        content = "".join(content)
        content = self.PreProcess(content)

        if(len(content) == 0):
          return

        print(post)
        print(title)
        # print("".join(content))
        dic['title'] = title[:-12]
        dic['content'] = content

        yield dic
        
    def PreProcess(self, text):
      text = re.sub(pattern='Posted on [0-9]{4} [0-9]{2} [0-9]{2} .+ Posted in \S+ \s?', repl='', string=text)
      _filter = re.compile('[ㄱ-ㅣ]+')
      text = _filter.sub('', text)
      _filter = re.compile('[^가-힣 0-9 a-z A-Z \. \, \" \? \! \n \r]+')
      text = _filter.sub('', text)
      _filter = re.compile('[\n\r]+')
      text = _filter.sub("", text)
      return text[43:-31]
