import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.utils.project import get_project_settings
from importlib import import_module


# Current script will automate re running procces

nm='ProfileScraper.ProfileScraper.spiders.akin'
imp = import_module(nm)
model = getattr(imp, "PersonProfileScraper")


process = CrawlerProcess(get_project_settings)

process.crawl(model)

process.start()
