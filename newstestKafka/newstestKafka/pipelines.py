# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from scrapy.exceptions import DropItem
from scrapy.utils.serialize import ScrapyJSONEncoder
from json import dumps
from kafka import KafkaProducer

class KafkaProducerPipeline(object):

    def __init__(self, kafka_bootstrap_server):
        self.kafka_bootstrap_server = []
        self.kafka_bootstrap_server.append(kafka_bootstrap_server)
        self.collection_name = 'articles'
        self.encoder = ScrapyJSONEncoder()

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            kafka_bootstrap_server = crawler.settings.get('KAFKA_BOOTSTRAP_SERVER'),
        )

    def open_spider(self, spider):
        print("spider name: ", spider.name)
        # initializing py-Kafka producer      
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_bootstrap_server)

        print("kafka_bootstrap_server: ", self.kafka_bootstrap_server)
        if hasattr(spider, 'collection_name'):
            print("spider collection_name: ", spider.collection_name)
            self.collection_name = spider.collection_name

    def close_spider(self, spider):
        # clean up when spider is closed
        self.producer.flush(timeout=60)
        self.producer.close(timeout=60)

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            print("valid - inside process_item...", item['source'], ': ',item['headline'])
            # self.producer.send('articles', self.encoder.encode(item).encode())
            key = str(ord(item['source'][0])) + str(ord(item['source'][1]))
            self.producer.send('articles', value=self.encoder.encode(item).encode(), key=key.encode())
            self.index += 1
            logging.debug("News item sent by Kafka Producer!")
        return item
