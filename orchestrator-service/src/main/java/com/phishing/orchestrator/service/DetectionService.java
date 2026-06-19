package com.phishing.orchestrator.service;

import com.phishing.orchestrator.dto.PredictionResponse;
import com.phishing.orchestrator.dto.UrlRequest;
import com.phishing.orchestrator.model.DetectionRecord;
import com.phishing.orchestrator.repository.DetectionRecordRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class DetectionService {

    private final DetectionRecordRepository repository;
    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${brain.api.url:http://localhost:8000/predict}")
    private String pythonApiUrl;

    public PredictionResponse detectPhishing(UrlRequest request) {
        try {
            // 1. Talk to Python Brain-API
            Map<String, String> pythonRequest = new HashMap<>();
            pythonRequest.put("url", request.getUrl());

            ResponseEntity<Map> pythonResponse = restTemplate.postForEntity(
                pythonApiUrl, 
                pythonRequest, 
                Map.class
            );

            Map<String, Object> body = pythonResponse.getBody();
            if (body == null) {
                throw new RuntimeException("Empty response body from Brain-API");
            }

            // 2. Extract Result from Python
            boolean isPhishing = (Boolean) body.getOrDefault("is_phishing", false);
            double confidence = ((Number) body.getOrDefault("confidence", 0.0)).doubleValue();
            String explanation = (String) body.getOrDefault("explanation", "Analysis complete");

            // 3. Save to Mongo with request.getType() (AUTO/MANUAL)
            DetectionRecord record = DetectionRecord.builder()
                .url(request.getUrl())
                .isPhishing(isPhishing)
                .confidence(confidence)
                .explanation(explanation)
                .checkSource(request.getType())
                .timestamp(LocalDateTime.now())
                .status("SUCCESS")
                .build();

            repository.save(record);

            // 4. Return to Controller
            return PredictionResponse.builder()
                .isPhishing(isPhishing)
                .confidence(confidence)
                .explanation(explanation)
                .build();

        } catch (Exception e) {
            log.error("Error during phishing check: {}", e.getMessage(), e);
            
            // Save error record to MongoDB
            try {
                DetectionRecord errorRecord = DetectionRecord.builder()
                    .url(request.getUrl())
                    .isPhishing(false)
                    .confidence(0.0)
                    .explanation("Brain-API error: " + e.getMessage())
                    .checkSource(request.getType())
                    .timestamp(LocalDateTime.now())
                    .status("ERROR")
                    .errorMessage(e.getMessage())
                    .build();
                repository.save(errorRecord);
            } catch (Exception ex) {
                log.error("Failed to save error record: {}", ex.getMessage());
            }

            return PredictionResponse.builder()
                .isPhishing(false)
                .confidence(0.0)
                .explanation("Brain-API is unreachable: " + e.getMessage())
                .build();
        }
    }
}