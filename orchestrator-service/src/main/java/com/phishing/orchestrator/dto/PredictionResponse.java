package com.phishing.orchestrator.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PredictionResponse {
    
    @JsonProperty("isPhishing")
    @JsonAlias("is_phishing")
    private boolean isPhishing;
    
    @JsonProperty("confidence")
    private double confidence;
    
    @JsonProperty("explanation")
    private String explanation;
}
