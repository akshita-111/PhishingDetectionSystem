#!/bin/bash

# Phishing Detection System - Clean Integration Script
# This script starts all services and tests the integration

echo "🔍 Starting Phishing Detection System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${RED}Port $1 is already in use${NC}"
        return 1
    else
        echo -e "${GREEN}Port $1 is available${NC}"
        return 0
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    echo -e "${BLUE}Waiting for $service_name to be ready...${NC}"

    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}$service_name is ready!${NC}"
            return 0
        fi
        echo -e "${YELLOW}Attempt $attempt/$max_attempts: $service_name not ready yet...${NC}"
        sleep 2
        ((attempt++))
    done

    echo -e "${RED}$service_name failed to start within expected time${NC}"
    return 1
}

# Check ports
echo "Checking port availability..."
check_port 8000 || exit 1
check_port 8080 || exit 1

# Start Brain API (Python)
echo -e "${BLUE}Starting Brain API (Python FastAPI)...${NC}"
cd brain-api
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BRAIN_PID=$!
cd ..

# Wait for Brain API
wait_for_service "http://localhost:8000/docs" "Brain API" || exit 1

# Start Orchestrator Service (Java)
echo -e "${BLUE}Starting Orchestrator Service (Spring Boot)...${NC}"
cd orchestrator-service
mvn spring-boot:run &
ORCHESTRATOR_PID=$!
cd ..

# Wait for Orchestrator Service
wait_for_service "http://localhost:8080/api/v1/health" "Orchestrator Service" || exit 1

echo -e "${GREEN}🎉 All services are running!${NC}"
echo ""
echo -e "${BLUE}Service URLs:${NC}"
echo "  🧠 Brain API:        http://localhost:8000"
echo "  🌐 Orchestrator API: http://localhost:8080"
echo "  🎨 Frontend:         http://localhost:8080"
echo ""
echo -e "${BLUE}Test the system:${NC}"
echo "  curl -X POST http://localhost:8080/api/v1/check -H 'Content-Type: application/json' -d '{\"url\":\"https://example.com\"}'"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Wait for user interrupt
trap "echo -e '${RED}Stopping services...${NC}'; kill $BRAIN_PID $ORCHESTRATOR_PID 2>/dev/null; exit 0" INT
wait