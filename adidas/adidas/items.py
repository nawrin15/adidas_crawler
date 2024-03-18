# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join

def get_sense_of_size(text):
    # print("%%%%%%", text.split('_'))
    return text.split('_')[-2:]
   
def add_base_url(url):
    return "https://shop.adidas.jp/"+url
 
class AdidasItem(scrapy.Item):
    url = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    breadcrumb = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=Join('/')
    )
    image_urls = scrapy.Field(
        input_processor=MapCompose(add_base_url),
        output_processor=Join(' , ')
    )
    category = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    product_name = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    sizes = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=Join(',')
    )
    sense_of_the_size = scrapy.Field(
        input_processor=MapCompose(get_sense_of_size),
        output_processor=Join('.')
    )
    title = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    general_description = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=Join('\n')
    )
    articleFeatures = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=Join('\n')
    )
    rating = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    number_of_reviews = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    recommended_rate = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )