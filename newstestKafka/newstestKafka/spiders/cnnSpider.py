import scrapy
import re
import json
import datetime
from newstestKafka.items import NewsItem


class CnnSpider(scrapy.Spider):
    # identifying information
    name = "cnn"
    allowed_domains = ["www.cnn.com"]
    start_urls = [
        "http://www.cnn.com", ]

    def parse(self, response):
        print("-----inside cnn-----")
        # extract data from javascript (json)
        data = re.findall("{\"articleList\":(.+?)}]}", response.body.decode("utf-8"), re.S)
        jsonData = json.loads("{\"articleList\":" + data[0] + "}]}")
        print("------------------------")
        for data in jsonData['articleList']:
            if data['duration'] == '':
                item = NewsItem()
                item['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                item['source'] = 'cnn'
                item['genre'] = 'news'
                item['headline'] = data['headline']
                item['url'] = "http://www.cnn.com" + data['uri']
                request = scrapy.Request(item['url'], callback=self.parse_url_page)
                request.meta['item'] = item
                yield request

    def parse_url_page(self, response):
        item = response.meta['item']
        text = ''
        lines = scrapy.selector.Selector(
            response).xpath('//*[@class="zn-body__paragraph speakable"] | //*[@class="zn-body__paragraph"]') 
        for line in lines:
            strline = str(line.xpath('text()').extract_first())
            if strline != 'None':
                text += strline + '\n'
        item['text'] = text
        yield item
                

