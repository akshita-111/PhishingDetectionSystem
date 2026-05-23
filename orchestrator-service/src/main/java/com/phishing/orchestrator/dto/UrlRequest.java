package com.phishing.orchestrator.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import javax.validation.constraints.NotBlank;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UrlRequest {
    private String url;
    private String type; // Expected: "AUTO" or "MANUAL"
}