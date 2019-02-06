from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
import logging

import sys
# The following line (which leads to the folder containing "scrapy.cfg") fixed the problem
sys.path.append('/home/barnwaldo/Workspace/Python/newstestKafka')

runner = CrawlerRunner(get_project_settings())

# running the spiders sequentially by chaining the deferreds


@defer.inlineCallbacks
def crawl():
    yield runner.crawl('cnn')
    print("1--CNN feed stored in MongoDB scrapyNews schema...")
    yield runner.crawl('foxnews')
    print("2--Fox News feed stored in MongoDB scrapyNews schema...")
    yield runner.crawl('reuters')
    print("3--Reuters feed stored in MongoDB scrapyNews schema...")
    yield runner.crawl('ap')
    print("4--AP News feed stored in MongoDB scrapyNews schema...")
    yield runner.crawl('cnbc')
    print("5--CNBC feed stored in MongoDB scrapyNews schema...")
    reactor.stop()


def main():
    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished


if __name__ == '__main__':
    main()
    print("NewsTest script is complete...")
