// Configuration for the browser extension
// Update these URLs based on your deployment environment

const CONFIG = {
  // Backend URL - Change this based on your environment
  // For local development: 'http://localhost:8080'
  // For production: 'https://orchestrator-services.onrender.com'
  BACKEND_URL: 'http://localhost:8080',
  
  // API endpoints
  API_URL: '', // Will be set based on BACKEND_URL
  HEALTH_URL: '' // Will be set based on BACKEND_URL
};

// Set API URLs based on backend URL
CONFIG.API_URL = `${CONFIG.BACKEND_URL}/api/v1/check`;
CONFIG.HEALTH_URL = `${CONFIG.BACKEND_URL}/api/v1/health`;
