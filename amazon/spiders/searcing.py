import scrapy
from utils.amazon import extractor, pagination

class SearchingSpider(scrapy.Spider):
    name = "searching"
    allowed_domains = ["amazon.com"]
    start_urls = ["https://www.amazon.com/s?k=suns+creame"]

    def parse(self, response):
        with open("amazon_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        # Yield extracted products
        yield from extractor(response)

        # Follow next page
        next_page = pagination(response)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
