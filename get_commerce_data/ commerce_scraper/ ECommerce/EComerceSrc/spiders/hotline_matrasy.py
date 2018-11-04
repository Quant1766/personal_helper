# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.item import Item, Field
from utils import CntUtils
from urlparse import urlparse
import os
import inspect
from scrapy.conf import settings
import requests
import random
import urllib2,urllib
from time import sleep
from EComerceScr import settings as seting_

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)


class ProductItem(Item):
    person_slug = Field()
    rating =Field()
    name = Field()
    title = Field()
    webpage = Field()
    category = Field()
    subcategory =Field()
    description = Field()
    series = Field()
    manufactyrer = Field()
    photo = Field()
    organization = Field()
    size = Field()
    value = Field()
    currency = Field()
    prices = Field()
    characteristics = Field()
    chart_price = Field()
    shops = Field()




class PersonProfileScraper(CrawlSpider):
    name = "ProfileScr2"
    allowed_domains = ["hotline.ua"]
    start_urls = ["https://hotline.ua/dom/"]


    parsed = urlparse(start_urls[0])
    output_file_name = os.path.join('results', parsed.hostname.replace("www.", "").replace(".", "_matrasy_33_2") + ".json")

    path_output_file_name = os.path.join(parentdir, output_file_name)
    settings.set('FILE_NAME', path_output_file_name)

    custom_settings = {
        'FILE_NAME': path_output_file_name,
        'DEPTH_LIMIT': 3
    }


    rules = [
        Rule(
            LinkExtractor(allow=("matrasy/",),
                          #tags=('div',),
                          #deny=("page/",),
                          #attrs=('data-link',),
                          restrict_xpaths=('//ul[@class="menu-in"]/li//a'),
                          canonicalize=True, unique=True),
            follow=True,
            callback='paginatoe'
        )
    ]

    def captcha_solve_cheker(self,response):
        try:
            captcha_key = response.xpath('//div[@id="g-recaptcha"]/@data-sitekey').extract_first()
            captcha_key = captcha_key if captcha_key else None
            if not captcha_key:
                return
            elif captcha_key:
                self.re_captcha2(captcha_key,response.url)
            return

        except:
            return



    def paginatoe(self,response):
        #self.captcha_solve_cheker(response)


        try:

            pages = int(response.xpath('//span[@class="pages"]/following-sibling::a[@class="pages"]//text()').extract_first().strip())
            for url_n in self.randit_list(pages,33,2):
                url_ = response.urljoin('?p={0}'.format(str(url_n)))

                yield scrapy.Request(url_, callback=self.get_products_links, dont_filter=True)
        except:
            yield scrapy.Request(response.url, callback=self.get_products_links, dont_filter=True)



    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, callback=self.get_products_links, dont_filter=True)

    def get_products_links(self,response):




        links = LinkExtractor(#allow=("author/",),
                              restrict_xpaths=('//ul[contains(@class,"products-list")]//li//p[@class="h4"]//a'),
                              #deny=("page/"),
            canonicalize=True, unique=True).extract_links(response)

        for url in links:
            yield scrapy.Request(url.url, callback=self.parse_items, dont_filter=True)

    def parse_items(self, response):
        #time.sleep(0.2)

        items = []

        item = ProductItem()

        try:
            ncsbs = [i.strip() for i in response.xpath('//ul[@class="breadcrumbs cell-12"]//a/text()|//ul[@class="breadcrumbs cell-12"]//li/span/text()').extract() if i]

            try:

                item['name'] = ncsbs[3]

            except:
                item['name'] = None

            try:

                item['category'] = ncsbs[0]

            except:
                item['category'] = None

            try:

                item['subcategory'] = ncsbs[1]

            except:
                item['subcategory'] = None


            try:

                item['manufactyrer'] = ncsbs[2]

            except:
                item['manufactyrer'] = None



        except:

            item['name'] = None


            item['category'] = None

            item['subcategory'] = None


            item['manufactyrer'] = None


        try:
            title = response.xpath('//article[@class="author-intro"]//h2//text()').extract_first().strip()
            item['title'] = title if title else None

        except:
            item['title'] = None

        item['webpage'] = response.url

        try:
            description = ' '.join([i.strip() for i in response.xpath('//div[@class="app-nav-scroll"]//div[@class="text"]//text()').extract()  if i.strip()]).strip()
            item['description'] = description if description else None
        except:
            item['description'] = None

        try:
            photo = response.xpath('//article[@class="author-intro"]//img/@src').extract_first()#.strip()#.split(' ')[0]

            item['photo'] = response.urljoin(photo) if 'team-placesholder' not  in photo else None
        except:
            item['photo'] = None


        item['person_slug'] = CntUtils.getuuid(response.url)

        item['organization'] = "Hotline.ua"
        try:
            rating = response.xpath('//span[@class="stars-box-width"]/@style').extract_first().split("width:")[1].split("%")[0].strip()

            item['rating'] = rating if rating else None
        except:
            item['rating'] = None

        try:
            characteristics = {}
            characteristic_article = response.xpath('//div[@data-pills="parent"]//div[@class="table-type-1"]/div')

            for charac in characteristic_article:
                try:

                    name_chara = ' '.join([i.strip() for i in charac.xpath('.//div[@class="table-cell cell-4"]//text()').extract() if i.strip()]).strip()
                    name_chara = name_chara if name_chara and len(name_chara)>1 else None
                    parametr = ' '.join([i.strip() for i in charac.xpath('.//div[@class="table-cell cell-8"]//text()').extract() if i.strip()]).strip()

                    parametr = parametr if parametr and len(parametr)>1 and len(name_chara)>1 else None


                    if name_chara and parametr:
                        characteristics[name_chara] = parametr

                except:
                    pass

            item['characteristics'] = characteristics if characteristics else None

        except:
            pass

        try:
            prices = response.xpath('//span[contains(@class,"price-lg pointer")]//span//text()').extract_first()
            item['prices'] = prices if prices else None
        except:
            item['prices'] = None

        try:
            currency = ' '.join([b.strip() for b in response.xpath('//span[contains(@class,"price-lg pointer")]/text()|//div[@class="resume-item resume-price"]//span[@class="price-format"]/text()').extract() if b.strip()])
            item['currency'] = currency if currency else None
        except:
            item['currency'] = None

        try:
            chart_num = ' '.join([b.strip() for b in response.xpath('//div[@class="cell-9 cell-lg"]/script[contains(.,"temp/charts")]//text()').extract()]).strip().split('chartAvgPriceUrl = "')[1].split('?rnd=')[0]
            headers = {'user-agent':seting_.USER_AGENT}
            chart_price = requests.get('http://hotline.ua/{0}'.format(chart_num),headers=headers)
            chart  = {}
            for i in chart_price.text.split():
                c_p = i.split(";")
                chart[c_p[0]] = c_p[1]
            item['chart_price'] = chart

        except:
            pass


        try:
            item['size'] = "New York, NY"
        except:
            item['size'] = None


        try:
            item['value'] = None
        except:
            item['value'] = None


        if item['name'] is not None and item['name'] != '':
            items.append(item)

        return items

    def re_captcha2(self,captcha_key,url="https://hotline.ua/"):

        print("captcha_key,url",captcha_key,url)

        API_KEY = '<API_KEY>'  # Your 2captcha API KEY

       # url = 'https://hotline.ua/'  # example url

        s = requests.Session()

        #resp = s.get('https://www.similarweb.com',proxies=self.proxies)


        #tree = html.fromstring(resp.text)



        capcha_key = captcha_key#tree.xpath('//iframe/@src')[0].split('fallback?k=')[1]  # .lower()

        captcha_id = s.post(
            "https://2captcha.com/in.php?key={0}&method=userrecaptcha&googlekey={1}&pageurl={2}".format(API_KEY, capcha_key,
                                                                                                  url),#proxies=self.proxies
        ).text.split('|')[1]

        recaptcha_answer = s.get("https://2captcha.com/res.php?key={0}&action=get&id={1}".format(API_KEY, captcha_id)#,proxies=self.proxies
                                 ).text
        while 'CAPCHA_NOT_READY' in recaptcha_answer:
            sleep(5)
            recaptcha_answer = s.get("https://2captcha.com/res.php?key={0}&action=get&id={1}".format(API_KEY, captcha_id)#,proxies=self.proxies
                                     ).text
        if 'ERROR_CAPTCHA_UNSOLVABLE' in recaptcha_answer:
            print('ERROR_CAPTCHA_UNSOLVABLE')
            return 0

        recaptcha_answer = recaptcha_answer.split('|')
        recaptcha_answer = recaptcha_answer[1:]

        payload_ = {'g-recaptcha-response': '|'.join(recaptcha_answer)}


        url_for_captcha = 'https://www.similarweb.com/distil_r_captcha.html?requestId={0}&httpReferrer=%2Fwebsite%2Fhingeto.com'.format(
            capcha_key)

        response = s.post(url_for_captcha, payload_)#,proxies=self.proxies)

        if len(response.cookies.get_dict())>1:
            print('Recaption')

    def randit_list(self,quanty,n,i):

        in_l = list(range(quanty/n*(i-1), ((quanty)/n)*i + 1))
        out_l = []
        while len(in_l) > 0:
            l = random.choice(in_l)
            out_l.append(l)
            in_l.remove(l)

        return out_l


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(PersonProfileScraper)
    process.start()
