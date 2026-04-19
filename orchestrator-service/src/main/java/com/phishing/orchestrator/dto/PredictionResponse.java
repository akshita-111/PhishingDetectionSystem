package com.phishing.orchestrator.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PredictionResponse {
    
    private boolean isPhishing;
    
    private double confidence;
    
    private String explanation;
}
