package com.phishing.orchestrator.repository;

import com.phishing.orchestrator.model.DetectionRecord;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface DetectionRecordRepository extends MongoRepository<DetectionRecord, String> {
    
    List<DetectionRecord> findByUrl(String url);
    
    List<DetectionRecord> findByTimestampBetween(LocalDateTime start, LocalDateTime end);
    
    List<DetectionRecord> findByIsPhishing(boolean isPhishing);
}
