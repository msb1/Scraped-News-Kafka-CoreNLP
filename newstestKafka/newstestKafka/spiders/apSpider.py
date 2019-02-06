import scrapy
import datetime
from newstestKafka.items import NewsItem


class ApSpider(scrapy.Spider):
    name = 'ap'
    allowed_domains = ['apnews.com']
    start_urls = ['https://apnews.com']

    def parse(self, response):
        print("-----inside apnews-----")
        articles = scrapy.selector.Selector(response).xpath('//a[@class="headline"]')
        print("------------------------")
        for article in articles:
            item = NewsItem()
            item['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            item['source'] = 'ap'
            item['genre'] = 'news'
            item['headline'] = article.xpath('h1/text()').extract_first()
            item['url'] = 'https://apnews.com' + article.xpath('@href').extract_first()
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
