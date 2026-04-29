package com.phishing.orchestrator.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Document(collection = "detection_records")
public class DetectionRecord {
    
    @Id
    private String id;
    
    private String url;
    
    private boolean isPhishing;
    
    private double confidence;
    
    private String explanation;
    
    private LocalDateTime timestamp;
    private String checkSource; // AUTO OR MANUAL 
   
    private String processingTimeMs;
    
    private String status; // SUCCESS, ERROR, TIMEOUT
    
    private String errorMessage;
}
