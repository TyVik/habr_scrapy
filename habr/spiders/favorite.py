from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from habr.items import HabrItem


class FavoriteSpider(CrawlSpider):
    name = "favorite"
    allowed_domains = ["habrahabr.ru"]
    start_urls = ["https://habrahabr.ru/users/tyvik/favorites/"]
    rules = (
        Rule(LinkExtractor(allow=('/page\d+/',)), callback='parse_page'),
    )

    def parse_page(self, response):
        root = Selector(response)
        # да, классы необходимо указывать полностью
        posts = root.xpath('//article[@class="post post_preview"]')
        for post in posts:
            item = HabrItem()
            item['title'] = post.xpath('.//a[@class="post__title_link"]/text()').extract()[0]
            item['author'] = post.xpath('.//span[@class="user-info__nickname user-info__nickname_small"]/text()').extract()[0]
            item['stars'] = post.xpath('.//span[@class="bookmark__counter js-favs_count"]/text()').extract()[0]
            yield item
