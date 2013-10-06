from scrapy.spider import BaseSpider
#from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from find_books.items import FindBooksItem
from scrapy.http import Request

class BookSpider(BaseSpider):
  name = 'amazon_books'
  allowed_domain = ['amazon.com']
  start_urls = [
      #'http://www.amazon.com/b/ref=s9_dnav_bw_ir02_b?_encoding=UTF8&node=15375251&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=0TYN24SYJKG6B3CFTDB8&pf_rd_t=101&pf_rd_p=1570621722&pf_rd_i=3839'
      'http://www.amazon.com/dp/1449355730'
      #'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/'
      ]

  base_url = 'http://www.amazon.com/dp/'

  asins_history = []


  def parse(self, response):
    #filename = 'Game_programming'
    #open(filename, 'wb').write(response.body)
    hxs = HtmlXPathSelector(response)

    item = FindBooksItem();
    tags = hxs.select('//meta[@name="keywords"]/@content').extract()

    bookAsin = response.url[-10:]
    if 'Computer Books' in tags[0] and bookAsin not in self.asins_history:
      #yield item(tags=tags)
      item['tags'] = tags
      self.asins_history.append(bookAsin)
    else:
      return

    try:
      title = hxs.select('//span[@id="btAsinTitle"][1]/text()').extract()
      #yield item(title=title)
      item['title'] = title
    except:
      #yield item(title=None)
      item['title'] = None

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

    #print 'aaaaaaaaaaaaaaaaaaaaa:', self.asins_history
    #yield item(url=response.url)
