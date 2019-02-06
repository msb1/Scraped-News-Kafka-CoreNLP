package com.barnwaldo.newskafkanlp.utils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;

import com.barnwaldo.newskafkanlp.model.NewsItem;
import com.barnwaldo.newskafkanlp.repository.NewsItemRepository;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JMessageConsumer implements Runnable {

    private final NewsItemRepository newsItemRepository;
    private final SentimentAnalyzer sentimentAnalyzer;
    private final ObjectMapper mapper;
    private final BlockingQueue<String> queue;
    private final List<String> stringStor;
    private final List<NewsItem> newsItemStor;

    public JMessageConsumer(NewsItemRepository newsItemRepository, BlockingQueue<String> queue) {

        this.newsItemRepository = newsItemRepository;
        this.queue = queue;
        sentimentAnalyzer = new SentimentAnalyzer();
        sentimentAnalyzer.initialize();
        mapper = new ObjectMapper();
        stringStor = new ArrayList<>();
        newsItemStor = new ArrayList<>();
    }

    @Override
    public void run() {
        try {
            while (true) {
                String jsonItemText = queue.take();
                NewsItem newsItem = mapper.readValue(jsonItemText, NewsItem.class);
                // System.out.println(newsItem.toString());
                // perform sentiment analysis with Stanford Core NLP Analyzer
                newsItem.setResult(sentimentAnalyzer.getSentimentResult(newsItem.getText()));
                // save news item with results to MongoDB
                newsItem = newsItemRepository.save(newsItem);
                System.out.println("------------------------------------------------------");
                System.out.println(newsItem.getSource() + "@" + newsItem.getDate() + ": " + newsItem.getHeadline()
                        + " -- sentiment = " + newsItem.getResult().getSentimentType());
                System.out.println("------------------------------------------------------");
                // add buffer to only run garbage collector every 1000 news items processed
                stringStor.add(jsonItemText);
                newsItemStor.add(newsItem);
                if (stringStor.size() > 1000) {
                    stringStor.clear();
                    newsItemStor.clear();
                }
            }
        } catch (InterruptedException | IOException e) {
            Thread.currentThread().interrupt();
        }

    }

}
