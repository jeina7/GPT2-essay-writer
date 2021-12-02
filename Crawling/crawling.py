import scrapy

class Spider(scrapy.Spider):
  name = "test"
  start_urls = ['https://teen.munjang.or.kr/archives/category/write/life']

  def parse(self, response):
    for post in response.css(''):
      next_post = post.css()

      if next_post is not None :
        next_post = response.urljoin(next_post)
        yield scrapy.Request(next_post, callback=self.parse_txt)

    next_page = response.css().extract_first()

    if next_page is not None:
      next_page = response.urljoin(next_page)
      yield scrapy.Request(next_page, callback=self.parse)

  def parse_text(self, response):
    for link in response.css('div.s_write'):
      post_link = response.url

      