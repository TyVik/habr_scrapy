from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from habr.items import HabrItem


class HabrSpider(CrawlSpider):
    name = "habr"
    allowed_domains = ["habrahabr.ru"]
    start_urls = [
        "https://habrahabr.ru"
    ]

    rules = (
        Rule(LinkExtractor(allow=('/page\d+/',)), callback='parse_item'),
    )

    def parse_item(self, response):
        root = Selector(response)
        posts = root.xpath('//div[@class="post post_teaser shortcuts_item"]')
        for post in posts:
            item = HabrItem()
            item['title'] = post.xpath('.//a[@class="post__title_link"]/text()').extract()[0]
            item['author'] = post.xpath('.//a[@class="post-author__link"]/text()')[1].extract().rstrip()
            item['stars'] = post.xpath('.//span[@class="favorite-wjt__counter js-favs_count"]/text()').extract()[0]
            yield item
