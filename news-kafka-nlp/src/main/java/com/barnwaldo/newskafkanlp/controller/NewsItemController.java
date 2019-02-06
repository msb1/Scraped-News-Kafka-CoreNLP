package com.barnwaldo.newskafkanlp.controller;

import java.util.Collection;
import java.util.stream.Collectors;

import org.springframework.web.bind.annotation.PathVariable;
//import org.springframework.web.bind.annotation.CrossOrigin;
//import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.barnwaldo.newskafkanlp.model.NewsItem;
import com.barnwaldo.newskafkanlp.repository.NewsItemRepository;

/**
 * Simple controller to show JSON items
 * 	
 * 	1) all news items
 * 	2) news items by source
 * 	3) news items by source and data
 * 	4) news items by keyword
 * 	5) news items by sources and keyword
 * 
 * @author barnwaldo
 * @version %I%, %G%
 *
 */
@RestController
public class NewsItemController {

	private final NewsItemRepository newsItemRepository;

	public NewsItemController(NewsItemRepository newsItemRepository) {
		this.newsItemRepository = newsItemRepository;
	}

	@RequestMapping(value = "/articles", method = RequestMethod.GET)
	public Collection<NewsItem> newsItems() {
		return newsItemRepository.findAll();
	}

	@RequestMapping(value = "/articles/{source}", method = RequestMethod.GET)
	public Collection<NewsItem> newsItemsBySource(@PathVariable String source) {
		return newsItemRepository.findBySource(source).stream().collect(Collectors.toList());
	}

	@RequestMapping(value = "/articles/{source}/{date}", method = RequestMethod.GET)
	public Collection<NewsItem> newsItemsBySourceDate(@PathVariable String source, @PathVariable String date) {
		return newsItemRepository.findBySource(source).stream().filter(item -> item.getDate().equals(date))
				.collect(Collectors.toList());
	}

	@RequestMapping(value = "/articles/keyword/{word}", method = RequestMethod.GET)
	public Collection<NewsItem> newsItemsByKeyword(@PathVariable String word) {
		return newsItemRepository.findAll().stream().filter(item -> item.getText().contains(word))
				.collect(Collectors.toList());
	}

	@RequestMapping(value = "/articles/keyword/{source}/{word}", method = RequestMethod.GET)
	public Collection<NewsItem> newsItemsByKeywordSource(@PathVariable String source, @PathVariable String word) {
		return newsItemRepository.findBySource(source).stream().filter(item -> item.getText().contains(word))
				.collect(Collectors.toList());
	}

}
