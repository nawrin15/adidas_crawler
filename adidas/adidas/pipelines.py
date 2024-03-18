# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import time
import os

from adidas.utils import get_project_root
root = str(get_project_root())


# CSV pipeline. the priority of this pipeline is set in the setting.py
class CsvPipeline(object):
    # set the path where the csv file will generate
    path = root + "/csv/"
    if not os.path.exists(path):
        os.makedirs(path)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        print("=====================spider open")
        # the file name coms from individual spider pages.
        self.fileName = self.path + \
            spider.settings.get('COLLECTION_NAME') + '-' + \
            str(int(time.time() * 1000)) + '.csv'
        self.file = open(self.fileName, 'a+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        print("=====================spider close")
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        print("=====================spider process")
        self.exporter.export_item(item)
        return item