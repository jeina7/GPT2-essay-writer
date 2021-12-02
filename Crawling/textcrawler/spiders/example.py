# -*- coding: utf-8 -*-
# http://sooyoung32.github.io/dev/2016/02/07/scrapy-tutorial.html
import scrapy

class Spider(scrapy.Spider):
  name = "textCrawler"
  start_urls = ['https://teen.munjang.or.kr/archives/category/write/life']
  result = {}

  def parse(self, response):
    # for post in response.xpath('//a'):
    n = 1
    for post in response.css('.post_title').xpath('//a'):
    # for post in response.css('.post_title').xpath('//a').get():
      # url = response.urljoin(post)
      # yield scrapy.Request(url, callback=self.parse_text)
      # print('post:',post)
    # url = response.urljoin(post.extract())
      # yield scrapy.Request(url, callback=self.parse_text)

  # def parse_text(self, response):
    # for post in response:
      # item = post.xpath('//p/text()').extract()//*[@id="uniform-breadcrumb"]/div/span
      # title = post.xpath('//header/h1/text()').extract()
      print(post)
      title = post.css('.entry-title').extract()
      # item = post.xpath('//p/text()').re('(\w+)')
      # item = post.xpath('//p/text()').extract()
      # print('item:',item)//*[@id="post-111089"]/header/h1
      print(title)
      # self.result[post] = item
      # yield dic
      n+=1
      if n== 3 :
        break
    yield self.result
# //*[@id="post-111089"]/div[1]/div/p[3]
# //*[@id="post-111089"]/div[1]/div/p[1]
#       if next_post is not None :
#         next_post = response.urljoin(next_post)
#         yield scrapy.Request(next_post, callback=self.parse_txt)

#     next_page = response.css().extract_first()

#     if next_page is not None:
#       next_page = response.urljoin(next_page)
#       yield scrapy.Request(next_page, callback=self.parse)

#   def parse_text(self, response):
#     for link in response.css('div.s_write'):
#       post_link = response.url


# //*[@id="post-111089"]/div/div[2]/div[1]/a
# //*[@id="post-106393"]/div/div[2]/div[1]/a
# /html/body/div[1]/div[3]/div[2]/div/main/article[1]/div/div[2]/div[1]/a
# //*[@id="post-111089"]/div/div[2]/div[1]/a