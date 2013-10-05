from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from find_books.items import FindBooksItem

class BookSpider(BaseSpider):
  name = 'amazon_books'
  allowed_domain = ['amazon.com']
  start_urls = [
      'http://www.amazon.com/b/ref=s9_dnav_bw_ir02_b?_encoding=UTF8&node=15375251&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=0TYN24SYJKG6B3CFTDB8&pf_rd_t=101&pf_rd_p=1570621722&pf_rd_i=3839'
      #'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/'
      ]

  def parse(self, response):
    #filename = 'Game_programming'
    #open(filename, 'wb').write(response.body)
    hxs = HtmlXPathSelector(response)
    bookNodes = hxs.select('//td[@class="dataColumn"]/table/tr/td')
    items = []
    for bookNode in bookNodes:
      item = FindBooksItem()
      #print bookNode
      title = bookNode.select('a/span/text()').extract()
      url = bookNode.select('a[1]/@href').extract()
      if len(title) > 0 and len(url) > 0:
        item['title'] = title
        item['url'] = url
        items.append(item)
    return items
