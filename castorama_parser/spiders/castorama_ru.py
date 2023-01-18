import scrapy
from scrapy.http import HtmlResponse
from items import CastoramaParserItem
# from castorama_parser.items import CastoramaParserItem
from scrapy.loader import ItemLoader


class CastoramaRuSpider(scrapy.Spider):
    name = 'castorama_ru'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

        links = response.xpath('//a[contains(@class, "product-card__name")]')
        for link in links:
            yield response.follow(link, callback=self.parse_castorama)

    def parse_castorama(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaParserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('price', '//div[contains(@class, "add-to-cart__price")]/div[contains(@class, "price-wrapper")]/div/div/div/span/span/span/span/text()')
        loader.add_xpath('photos', '//img[contains(@class, "thumb-slide__img")]/@data-src')
        yield loader.load_item()
        # product_name = response.xpath('//h1/text()').get()
        # product_url = response.url
        # price_and_currency = response.xpath(
        #     '//div[contains(@class, "add-to-cart__price")]/div[contains(@class, "price-wrapper")]/div/div/div/span/span/span/span/text()'
        # ).getall()
        # photos = response.xpath('//img[contains(@class, "thumb-slide__img")]/@data-src').getall()
        #
        # yield CastoramaParserItem(
        #     name=product_name,
        #     url=product_url,
        #     price=price_and_currency,
        #     photos=photos
        # )
