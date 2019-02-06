import scrapy
import datetime
from newstestKafka.items import NewsItem


class CnbcSpider(scrapy.Spider):
    name = 'cnbc'
    allowed_domains = ['www.cnbc.com']
    start_urls = ['https://www.cnbc.com']

    def parse(self, response):
        print("-----inside cnbc-----")
        articles = scrapy.selector.Selector(response).xpath("//div")  
        print("------------------------")
        for article in articles:
            item = NewsItem()
            url = article.xpath('a/@href').extract_first()
            if url is None or "video" in url or not str(datetime.datetime.now().year) in url:
                continue 
            item['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            item['source'] = 'cnbc'
            item['genre'] = 'business'
            item['headline'] = article.xpath('a/text()').extract_first().strip()
            item['url'] = 'https://www.cnbc.com' + url
            request = scrapy.Request(item['url'], callback=self.parse_url_page)
            request.meta['item'] = item
            yield request

    def parse_url_page(self, response):
        item = response.meta['item']
        text = ''
        lines = scrapy.selector.Selector(response).xpath('//p')
        for line in lines:
            strline = str(line.xpath('text()').extract_first()).strip()
            if strline == ('None' or ''):
                continue
            text += strline + '\n'
        item['text'] = text
        yield item
