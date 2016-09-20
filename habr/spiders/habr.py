from scrapy.spiders import CrawlSpider


class HabrSpider(CrawlSpider):
    name = "habr"  # имя для crawl команды
    allowed_domains = ["habrahabr.ru"]  # на страницы с каких сайтов переходить
    start_urls = [
        "http://habrahabr.ru"  # откуда начинать
    ]

    def parse(self, response):  # метод обработки ответа
        with open('response.html', 'wb') as f:
            f.write(response.body)