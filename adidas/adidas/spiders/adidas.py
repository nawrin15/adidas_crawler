import scrapy
from scrapy.loader import ItemLoader
import json
from adidas.items import AdidasItem


class Adidas(scrapy.Spider):
    name = 'adidas'
    # allowed_domains = ['']
    custom_settings = {
        'COLLECTION_NAME': 'adidas',
    }

    def start_requests(self):
        url = "https://shop.adidas.jp/f/v1/pub/product/list?gender=mens&page=1"

        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_items
        )

    def parse_items(self, response):
        response = json.loads(response.text)
        urls = [f"https://shop.adidas.jp/products/{item_id}" for item_id in response['articles_sort_list']]
        for url in urls:
            yield scrapy.Request(url, method="GET", callback=self.parse_item)


    def parse_item(self, response):
        loader = ItemLoader(item=AdidasItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('breadcrumb', "//ul[contains(@class, 'breadcrumbList')]/li/a/text()")
        loader.add_xpath('image_urls', "//div[contains(@class, 'article_image')]//img[contains(@class, 'test-img')]/@src")
        loader.add_xpath('category', "//span[contains(@class, 'categoryName')]//text()")
        loader.add_xpath('product_name', "//h1[contains(@class, 'itemTitle')]/text()")
        loader.add_xpath('price', "//div[contains(@class,'articlePrice')]//text()")
        loader.add_xpath('sizes', "//li[contains(@class,'sizeSelectorList')]//text()")
        loader.add_xpath('sense_of_the_size', "//div[contains(@class,'sizeFitBar')]/div/span/@class")
        loader.add_xpath('title', "//h4[contains(@class,'heading')]//text()")
        loader.add_xpath('general_description', "//div[contains(@class,'description_part')]//text()")
        loader.add_xpath('article_features', "//li[contains(@class,'articleFeatures')]//text()")
        loader.add_xpath('rating', "//div[@class='BVRRQuickTakeCustomWrapper']//span[contains(@class, 'BVRRRatingNumber')]//text()")
        loader.add_xpath('number_of_reviews', "//div[@class='BVRRQuickTakeCustomWrapper']//span[@class='BVRRNumber BVRRBuyAgainTotal']//text()")
        loader.add_xpath('recommended_rate', "//div[@class='BVRRQuickTakeCustomWrapper']//span[@class='BVRRBuyAgainPercentage']//text()")


        yield loader.load_item()