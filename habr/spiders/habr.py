from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector

from habr.items import HabrItem


class HabrSpider(CrawlSpider):
    name = "habr"  # имя для crawl команды
    allowed_domains = ["habrahabr.ru"]  # на страницы с каких сайтов переходить
    start_urls = [
        "http://habrahabr.ru"  # откуда начинать
    ]

    def parse(self, response):
        root = Selector(response)
        # да, классы необходимо указывать полностью
        posts = root.xpath('//div[@class="post post_teaser shortcuts_item"]')
        for post in posts:
            item = HabrItem()
            item['title'] = post.xpath('.//a[@class="post__title_link"]/text()').extract()[0]
            item['author'] = post.xpath('.//a[@class="post-author__link"]/text()')[1].extract().rstrip()
            item['stars'] = post.xpath('.//span[@class="favorite-wjt__counter js-favs_count"]/text()').extract()[0]
            yield item
