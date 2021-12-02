# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
# from scrapy.conf import settings
from scrapy.exceptions import DropItem
# from scrapy import log

class TextcrawlerPipeline(object):
    def __init__(self):
        file_name = "storyCrawl.csv"
        self.file = open(file_name, 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
