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
import java.time.Duration;

@Service
@RequiredArgsConstructor
@Slf4j
@Service
public class DetectionService {

    @Autowired
    private DetectionRepository repository;

    private final RestTemplate restTemplate = new RestTemplate();
    private final String PYTHON_API_URL = "http://localhost:8000/predict";

    public DetectionResponse processUrl(UrlRequest request) {
        try {
            // 1. Talk to Python Brain-API
            // We wrap the URL in a simple Map to send as JSON
            Map<String, String> pythonRequest = new HashMap<>();
            pythonRequest.put("url", request.getUrl());

            ResponseEntity<Map> pythonResponse = restTemplate.postForEntity(
                PYTHON_API_URL, 
                pythonRequest, 
                Map.class
            );

            Map<String, Object> body = pythonResponse.getBody();

            // 2. Extract Result from Python
            String result = (Boolean) body.get("is_phishing") ? "PHISHING" : "SAFE";
            double confidence = (Double) body.get("confidence");

            // 3. Save to Mongo with request.getType() (AUTO/MANUAL)
            DetectionRecord record = new DetectionRecord();
            record.setUrl(request.getUrl());
            record.setResult(result);
            record.setConfidence(confidence);
            record.setCheckSource(request.getType()); // This tracks AUTO vs MANUAL
            record.setTimestamp(LocalDateTime.now());

            repository.save(record);

            // 4. Return to Extension
            return new DetectionResponse(result, confidence, "Analysis complete via " + request.getType() + " mode.");

        } catch (Exception e) {
            // Graceful error handling if Python API is down
            return new DetectionResponse("ERROR", 0.0, "Brain-API is unreachable: " + e.getMessage());
        }
    }
}