package com.barnwaldo.newskafkanlp.model;

import lombok.*;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Getter
@Setter
@Document(collection = "articles")
@JsonInclude(JsonInclude.Include.NON_NULL)
public class NewsItem {
    
    private static final Logger logger = LoggerFactory.getLogger(NewsItem.class);

    @Id
    private String _id;
    private String date;
    private String headline;
    private String url;
    private String source;
    private String genre;
    private String text;
    private SentimentResult result;

    @Override
    public String toString() {
        ObjectMapper mapper = new ObjectMapper();

        String jsonString = "";
        try {
            mapper.enable(SerializationFeature.INDENT_OUTPUT);
            jsonString = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(this);
        } catch (JsonProcessingException e) {
            logger.error(e.getMessage());
        }
        return jsonString;
    }
}
