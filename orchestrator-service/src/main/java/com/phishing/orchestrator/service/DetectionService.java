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

@Service
@RequiredArgsConstructor
@Slf4j
public class DetectionService {

    private final RestTemplate restTemplate;
    private final DetectionRecordRepository detectionRecordRepository;


    @Value("${brain.api.url:http://localhost:8000/predict}")
    private String brainApiUrl;

    public PredictionResponse detectPhishing(UrlRequest urlRequest) {
        log.info("Starting phishing detection for URL: {}", urlRequest.getUrl());
        long startTime = System.currentTimeMillis();
        
        try {
            // Prepare request to brain API
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<UrlRequest> entity = new HttpEntity<>(urlRequest, headers);
            
            // Call brain API
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
                
                // Save detection record
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
                log.info("Successfully saved detection record for URL: {}", urlRequest.getUrl());
                
                return prediction;
            } else {
                throw new RuntimeException("Invalid response from brain API");
            }
            
        } catch (Exception e) {
            long processingTime = System.currentTimeMillis() - startTime;
            log.error("Error during phishing detection for URL {}: {}", urlRequest.getUrl(), e.getMessage());
            
            // Save error record
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
            
            // Return default response
            return PredictionResponse.builder()
                .isPhishing(false)
                .confidence(0.0)
                .explanation("Detection service temporarily unavailable")
                .build();
        }
    }
}
