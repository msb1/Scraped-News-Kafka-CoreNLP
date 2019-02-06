package com.barnwaldo.newskafkanlp;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.springframework.kafka.annotation.KafkaListener;

import com.barnwaldo.newskafkanlp.repository.NewsItemRepository;
import com.barnwaldo.newskafkanlp.utils.JMessageConsumer;

@SpringBootApplication
@EnableMongoRepositories(basePackageClasses = NewsItemRepository.class)
public class NewsKafkaNlpApplication {

    private BlockingQueue<String> queue;
    private static final Logger logger = LoggerFactory.getLogger(NewsKafkaNlpApplication.class);

    public static void main(String[] args) {
        SpringApplication.run(NewsKafkaNlpApplication.class, args);
    }

    @KafkaListener(topics = "articles", groupId = "Barnwaldo")
    public void listen(ConsumerRecord<?, ?> record) {
        System.out.println("Received Messasge: Key = " + record.key() + " -- Message: " + record.value());
        try {
            queue.put((String) record.value());
        } catch (InterruptedException e) {
            logger.error("Put message to queue failure - InterruptedException exerted...");
        }
    }

    @Bean
    ApplicationRunner init(NewsItemRepository newsItemRepository) {
        // return main class args & use Application Runner to start Consumer Thread
        return args -> {
            queue = new ArrayBlockingQueue<>(1024);
            JMessageConsumer consumerThread = new JMessageConsumer(newsItemRepository, queue);

            Thread consumer = new Thread(consumerThread);
            consumer.start();
        };
    }
}

