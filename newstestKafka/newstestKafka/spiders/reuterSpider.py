import scrapy
import datetime
from newstestKafka.items import NewsItem


class ReuterSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['www.reuters.com']
    start_urls = ['https://www.reuters.com']

    def parse(self, response):
        print("-----inside reuters-----")
        articles1 = scrapy.selector.Selector(response).xpath('//div[@class="feature"]')
        articles2 = scrapy.selector.Selector(response).xpath('//div[@class="story-content"]')
        print("------------------------")
        for article in articles1:
            item = NewsItem()
            try:
                item['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                item['source'] = 'reuters'
                item['genre'] = 'news'
                item['headline'] = article.xpath('div/a/div/h2/text()').extract_first()
                item['url'] = "https:" + article.xpath('div/a/@href').extract_first()
                item['headline'] = item['headline'].strip()
            except TypeError:
                continue
            request = scrapy.Request(item['url'], callback=self.parse_url_page)
            request.meta['item'] = item
            yield request

        for article in articles2:
            item = NewsItem()
            try:
                item['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                item['source'] = 'reuters'
                item['genre'] = 'news'
                item['headline'] = article.xpath('a/*/text() | */a/text() ').extract_first()
                item['url'] = "https://www.reuters.com" + article.xpath('a/@href | */a/@href').extract_first()
                item['headline'] = item['headline'].strip()
            except TypeError:
                continue
            request = scrapy.Request(item['url'], callback=self.parse_url_page)
            request.meta['item'] = item
            yield request

    def parse_url_page(self, response):
        item = response.meta['item']
        text = ''
        lines = scrapy.selector.Selector(response).xpath(
            '//div[@class="StandardArticleBody_body"]/p')
        for line in lines:
            strline = str(line.xpath('text()').extract_first()).strip()
            if strline != ('None' or ''):
                text += strline + '\n'
        item['text'] = text
        # with open('reuters.txt', 'a') as reuters:
        #     reuters.write("({}) {} -- url: {} \n {} \n".format(item['artId'], item['headline'], item['url'], item['text']))
        yield item
