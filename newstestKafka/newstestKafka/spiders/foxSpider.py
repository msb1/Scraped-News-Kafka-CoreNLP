import scrapy
import datetime
from newstestKafka.items import NewsItem


class FoxSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['www.foxnews.com']
    start_urls = ['https://www.foxnews.com']

    def parse(self, response):
        print("-----inside foxnews-----")
        articles = scrapy.selector.Selector(response).xpath('//h2[@class="title"]')
        print("------------------------")
        for article in articles:
            item = NewsItem()
            item['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            item['source'] = 'foxnews'
            item['genre'] = 'news'
            item['headline'] = article.xpath('a/text()').extract_first()
            item['url'] = "https:" + article.xpath('a/@href').extract_first()
            request = scrapy.Request(item['url'], callback=self.parse_url_page)
            request.meta['item'] = item
            yield request

    def parse_url_page(self, response):
        item = response.meta['item']
        text = ''
        lines = scrapy.selector.Selector(response).xpath('//p')
        for line in lines:
            strline = str(line.xpath('text()').extract_first()).strip()
            if strline != ('None' or ''):
                text += strline + '\n'
        item['text'] = text
        yield item
