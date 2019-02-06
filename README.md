### Scraped-News-Kafka-CoreNLP

news-nlp-kafka -- Spring Boot application with Kafka Consumer and write to MongoDB

* Spring Boot application is Kafka consumer for scraped website JSON data
* Stanford NLP Sentiment Analysis is performed on text from each new entry in DB -- model training is not required with CoreNLP sentiment analyzer
* Each entry is inserted to Mongo DB after sentiment analysis has been performed
* Restful controller is employed to easily view and sort JSON news source data
* Mongo Compass or Robo3T can also be used to monitor and examine news feed data that has been processed

newstestKafka -- Python script to generate news feed data

* Currently scrapes 5 newsites (but more can be readily added)
* Main program is script that sequentially performs newsite analyses
* Ethical scraping is performed; robots.txt and other ethical features are implemented
* Scraped items are JSON serialized and the sent to Kafka server using Kafka-python from the Scrapy pipeline

Note: Both Kafka Broker and Mongo DB are a standalone instances; they are not embedded in the Spring Boot App