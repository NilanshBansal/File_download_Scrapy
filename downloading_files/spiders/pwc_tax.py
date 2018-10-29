import urllib
import scrapy

from scrapy.http import Request

class pwc_tax(scrapy.Spider):
  name = "pwc_tax"

  allowed_domains = ["www.pwc.com"]
  start_urls = ["https://www.pwc.com/us/en/services/consulting/analytics/benchmarking-services.html"]

  def parse(self, response):
    base_url = 'https://www.pwc.com'

    for a in response.xpath('//a[@href]/@href'):
        link = a.extract()
        # self.logger.info(link)

        if link.endswith('.pdf'):
            link = urllib.parse.urljoin(base_url, link)
            self.logger.info(link)
            yield Request(link, callback=self.save_pdf)

  def save_pdf(self, response):
    path = response.url.split('/')[-1]
    self.logger.info('Saving PDF %s', path)
    with open(path, 'wb') as f:
        f.write(response.body)
