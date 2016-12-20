from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from habr.items import HabrItem


class FavoriteSpider(CrawlSpider):
    name = "favorite"
    allowed_domains = ["habrahabr.ru"]
    login_page = 'https://id.tmtm.ru/login/?state=0d67dc108cbf446f83f8de6b43c8c205&consumer=habrahabr'
    start_urls = ["https://habrahabr.ru/users/tyvik/favorites/"]
    rules = (
        Rule(LinkExtractor(allow=('/page\d+/',)), callback='parse_item'),
    )

    def start_requests(self):
        yield Request(self.login_page, callback=self.login)

    def login(self, response):
        return FormRequest.from_response(response,
                                         formdata={'email': 'tyvik8@gmail.com', 'password': 'password'},
                                         callback=self.check_login_response)

    def check_login_response(self, response):
        if b'<span class="user-info__nickname">TyVik</span>' in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            return [Request(url=u) for u in self.start_urls]
        else:
            self.log("Bad times :(")

    def parse_item(self, response):
        root = Selector(response)
        posts = root.xpath('//div[@class="post post_teaser shortcuts_item"]')
        for post in posts:
            item = HabrItem()
            item['title'] = post.xpath('.//a[@class="post__title_link"]/text()').extract()[0]
            item['author'] = post.xpath('.//a[@class="post-author__link"]/text()')[1].extract().rstrip()
            item['stars'] = post.xpath('.//span[@class="favorite-wjt__counter js-favs_count"]/text()').extract()[0]
            yield item
