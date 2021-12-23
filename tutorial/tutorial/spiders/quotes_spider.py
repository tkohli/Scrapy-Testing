import scrapy
from..items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/'
        ]
        # for i in range(1, 26):
        #     urls.append(
        #         "https://www.net-a-porter.com/en-in/shop/clothing/tops?pageNumber="+str(i))
        # for i in range(1, 26):
        #     urls.append(
        #         "https://www.net-a-porter.com/en-in/shop/shoes?pageNumber="+str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # title = response.css('title::text').get()
        # yield {'title': title}
        # for quote in range(50):
        # items['Titles'] = title
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
