from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


# Using the Spider class provided by the 'scrapy' package
class ModSpider(scrapy.Spider):
    name = "spider"
    start_urls = ['http://www.google.com']

    # Configure Setting for main driver code
    configure_logging()
    runner = CrawlerRunner()

    def crawl(self):
        self.crawl(ModSpider)
        reactor.stop()
    crawl()
    reactor.run()
    # the script will block here until the last crawl call is finished

    # SETTING_SELECTOR instructs spider which 'key word' to use when parsing the data
    # NAME_SELECTOR is the <HTML> tag to search within
    # The Object we are iterating over has its own CSS Method so we pass a selector element
    # to parse out child elements.
    def parse(self, response):
        SETTING_SELECTOR = '.set'
        for k in response.css(SETTING_SELECTOR):
            pass
            NAME_SELECTOR = 'h1:: text'
            yield {
                'name': k.css(NAME_SELECTOR).extract_first(),
            }
        # We define a selector for the next_page element (link), extract first match
        # and check to see if it exists.
        NEXT_PAGE_SELECT = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECT).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
