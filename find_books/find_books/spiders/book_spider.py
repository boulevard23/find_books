from scrapy.spider import BaseSpider
#from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from find_books.items import FindBooksItem
from scrapy.http import Request
import re

class BookSpider(BaseSpider):
  name = 'amazon_books'
  allowed_domain = ['amazon.com']
  start_urls = [
      'http://www.amazon.com/dp/0131103628'
      #'http://www.amazon.com/dp/032122731X'
      ]

  base_url = 'http://www.amazon.com/dp/'

  rating_pattern = re.compile('(\d\.?\d?) out of \d\.?\d? stars')
  asins_history = []


  def parse(self, response):
    hxs = HtmlXPathSelector(response)

    item = FindBooksItem();
    tags = hxs.select('//meta[@name="keywords"]/@content').extract()
    bookAsin = response.url[-10:]

    ratingSpan = hxs.select('//span[@class="crAvgStars"]//span[@name="' + bookAsin + '"]')
    ratingStr = ratingSpan.select('.//a//span/@title')[0]
    rating = float(ratingStr.re(self.rating_pattern)[0])
    reviewStr = ratingSpan.select('../a/text()').extract()[0]
    reviewsNum = int(reviewStr.split(' ')[0])
    print 'rating:', rating
    print 'reviews num:', reviewsNum

    if bookAsin not in self.asins_history and 'Computer Books' in tags[0] and rating >= 4.0 and reviewsNum >= 40:
      item['tags'] = tags
      item['amazonRating'] = rating
      item['reviewsNum'] = reviewsNum
      self.asins_history.append(bookAsin)
    else:
      return

    try:
      title = hxs.select('//span[@id="btAsinTitle"][1]/text()').extract()[0].strip()
    except:
      title = hxs.select('//h1[@id="title"][1]/text()').extract()[0].strip()
    item['title'] = title

    item['url'] = response.url

    try:
      asins = hxs.select('//div[@id="purchaseSimsData"]/text()').extract()
      #print 'asins: ', asins[0].split(',')
      item['asins'] = asins[0].split(',')
    except:
      item['asins'] = []
    yield item

    for asin in item['asins']:
      print 'asin', asin
      yield Request(self.base_url + asin, callback=self.parse)
