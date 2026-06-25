package com.phishing.orchestrator.controller;

import com.phishing.orchestrator.dto.PredictionResponse;
import com.phishing.orchestrator.dto.UrlRequest;
import com.phishing.orchestrator.service.DetectionService;
import javax.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class PhishingController {

    private final DetectionService detectionService;

    @PostMapping("/check")
    public ResponseEntity<PredictionResponse> checkPhishing(@Valid @RequestBody UrlRequest urlRequest) {
        log.info("Received phishing check request for URL: {}", urlRequest.getUrl());
        
        try {
            PredictionResponse response = detectionService.detectPhishing(urlRequest);
            log.info("Phishing check completed for URL: {}, isPhishing: {}, confidence: {}", 
                urlRequest.getUrl(), response.isPhishing(), response.getConfidence());
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            log.error("Error processing phishing check request: {}", e.getMessage());
            
            // Return error response
            PredictionResponse errorResponse = PredictionResponse.builder()
                .isPhishing(false)
                .confidence(0.0)
                .explanation("Service temporarily unavailable")
                .build();
            
            return ResponseEntity.status(500).body(errorResponse);
        }
    }

    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Orchestrator service is healthy");
    }
}
