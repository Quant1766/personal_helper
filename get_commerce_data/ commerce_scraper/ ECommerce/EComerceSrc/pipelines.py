# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter,CsvItemExporter
import csv
import json
import codecs
from collections import OrderedDict

ids_seen = set()

class DuplicatesPipeline(object):

    def __init__(self):
         self.profile_seen = set()

    def process_item(self, item, spider):
        if item['webpage'] in self.profile_seen or item['name']==None:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.profile_seen.add(item['webpage'])
            return item


class ProfilescraperPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        file_name = settings.get("FILE_NAME")
        return cls(file_name)


    def __init__(self,file_name):
        #name=spider.name+".json"
        name='test.json'
        #name = 'test.csv'
        self.file = open(file_name, 'wb')
        #self.exporter = CsvItemExporter(self.file,encoding='utf-8')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
