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
import javax.annotation.PostConstruct;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
@Slf4j
public class DetectionService {

    private final RestTemplate restTemplate;
    private final DetectionRecordRepository detectionRecordRepository;

    @Value("${brain.api.url:http://localhost:8000/predict}")
    private String brainApiUrl;

    @PostConstruct
    public void init() {
        if (brainApiUrl != null && !brainApiUrl.endsWith("/predict")) {
            if (brainApiUrl.endsWith("/")) {
                brainApiUrl = brainApiUrl + "predict";
            } else {
                brainApiUrl = brainApiUrl + "/predict";
            }
        }
        log.info("Initialized brain API URL to: {}", brainApiUrl);
    }

    public PredictionResponse detectPhishing(UrlRequest urlRequest) {
        log.info("Starting phishing detection for URL: {}", urlRequest.getUrl());
        long startTime = System.currentTimeMillis();
        
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<UrlRequest> entity = new HttpEntity<>(urlRequest, headers);
            
            log.info("Calling brain API at: {}", brainApiUrl);
            ResponseEntity<PredictionResponse> response = restTemplate.exchange(
                brainApiUrl,
                HttpMethod.POST,
                entity,
                PredictionResponse.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                PredictionResponse prediction = response.getBody();
                long processingTime = System.currentTimeMillis() - startTime;
                
                DetectionRecord record = DetectionRecord.builder()
                    .url(urlRequest.getUrl())
                    .isPhishing(prediction.isPhishing())
                    .confidence(prediction.getConfidence())
                    .explanation(prediction.getExplanation())
                    .timestamp(LocalDateTime.now())
                    .processingTimeMs(String.valueOf(processingTime))
                    .status("SUCCESS")
                    .build();
                
                detectionRecordRepository.save(record);
                log.info("Detection record saved successfully");
                return prediction;
            } else {
                throw new RuntimeException("Invalid response from brain API");
            }
            
        } catch (Exception e) {
            long processingTime = System.currentTimeMillis() - startTime;
            log.error("Error during phishing detection: {}", e.getMessage());
            
            DetectionRecord errorRecord = DetectionRecord.builder()
                .url(urlRequest.getUrl())
                .isPhishing(false)
                .confidence(0.0)
                .explanation("Error occurred during detection")
                .timestamp(LocalDateTime.now())
                .processingTimeMs(String.valueOf(processingTime))
                .status("ERROR")
                .errorMessage(e.getMessage())
                .build();
            
            detectionRecordRepository.save(errorRecord);
            
            return PredictionResponse.builder()
                .isPhishing(false)
                .confidence(0.0)
                .explanation("Detection service temporarily unavailable")
                .build();
        }
    }
}