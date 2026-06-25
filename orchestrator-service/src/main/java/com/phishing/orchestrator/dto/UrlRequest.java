package com.phishing.orchestrator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class UrlRequest {
    
    @JsonProperty("url")
    private String url;
    
    @JsonProperty("type")
    private String type; // Expected: "AUTO" or "MANUAL"

    public UrlRequest() {
    }

    public UrlRequest(String url, String type) {
        this.url = url;
        this.type = type;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}