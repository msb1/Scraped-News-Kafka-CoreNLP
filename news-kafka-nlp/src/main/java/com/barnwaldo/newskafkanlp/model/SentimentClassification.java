package com.barnwaldo.newskafkanlp.model;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import lombok.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Getter
@Setter
public class SentimentClassification {

    /*
	 * "Very negative" = 0 
	 * "Negative" = 1 
	 * "Neutral" = 2 
	 * "Positive" = 3
	 * "Very positive" = 4
     */

    private static final Logger logger = LoggerFactory.getLogger(SentimentClassification.class);
    
    private int veryPositive;
    private int positive;
    private int neutral;
    private int negative;
    private int veryNegative;

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
