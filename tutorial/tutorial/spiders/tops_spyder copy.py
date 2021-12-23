import scrapy
from..items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = "shoes"

    def start_requests(self):
        urls = [
            'https://www.net-a-porter.com/en-in/shop/shoes?pageNumber=1'
        ]
        # for i in range(2, 27):
        #     urls.append(
        #         "https://www.net-a-porter.com/en-in/shop/clothing/tops?pageNumber="+str(i))
        for i in range(2, 26):
            urls.append(
                "https://www.net-a-porter.com/en-in/shop/shoes?pageNumber="+str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # title = response.css('title::text').get()
        # yield {'title': title}
        # for quote in range(50):
        # items['Titles'] = title
        for quote in response.css('div.ProductItem24__p'):
            yield {
                'name': quote.css('.ProductItem24__designer::text').get(),
                'brand': quote.css('.ProductItem24__name::text').get(),
                'price': quote.css('span::text')[2].get(),
                'sale_price': quote.css('span::text')[2].get(),
                'image_url': response.css('img').xpath('@src').get(),
                'product_page_url': response.css(".ProductGrid52 a::attr(href)").get()

                # 'author': quote.css('small.author::text').get(),
                # 'tags': quote.css('div.tags a.tag::text').getall(),original_price
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
