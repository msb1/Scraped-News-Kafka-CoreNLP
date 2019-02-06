package com.barnwaldo.newskafkanlp.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import com.barnwaldo.newskafkanlp.model.NewsItem;

/**
 * Simple Spring Repository to access Mongo Database -- custom methods added to
 * find by news sources, news genre and data
 *
 * @author barnwaldo
 * @version %I%, %G%
 *
 */
public interface NewsItemRepository extends MongoRepository<NewsItem, String> {

    List<NewsItem> findBySource(String source);

    List<NewsItem> findByGenre(String genre);

    List<NewsItem> findByDate(String date);

}
