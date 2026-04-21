// Popup script

const API_URL = 'http://localhost:8080/api/v1/check';
const HEALTH_URL = 'http://localhost:8080/api/v1/health';

// Check service health
async function checkServiceHealth() {
  try {
    const response = await fetch(HEALTH_URL);
    return response.ok;
  } catch (error) {
    return false;
  }
}

// Update status display
async function updateStatus() {
  const statusDiv = document.getElementById('status');
  const statusText = document.getElementById('statusText');

  const isHealthy = await checkServiceHealth();

  if (isHealthy) {
    statusDiv.className = 'status active';
    statusText.textContent = '✅ Service Active';
  } else {
    statusDiv.className = 'status inactive';
    statusText.textContent = '❌ Service Offline';
  }
}

// Check phishing for a URL
async function checkPhishing(url) {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error checking phishing:', error);
    return { error: error.message };
  }
}

// Display result
function displayResult(result) {
  const resultDiv = document.getElementById('result');
  const resultText = document.getElementById('resultText');

  if (result.error) {
    resultDiv.className = 'result error';
    resultText.textContent = `Error: ${result.error}`;
  } else {
    const confidencePercent = Math.round(result.confidence * 100);

    if (result.isPhishing) {
      resultDiv.className = 'result phishing';
      resultText.textContent = `⚠️ Phishing detected! Confidence: ${confidencePercent}%`;
    } else {
      resultDiv.className = 'result safe';
      resultText.textContent = `✅ URL appears safe. Confidence: ${confidencePercent}%`;
    }
  }

  resultDiv.style.display = 'block';
}

// Handle check button click
document.getElementById('checkButton').addEventListener('click', async () => {
  const urlInput = document.getElementById('urlInput');
  const checkButton = document.getElementById('checkButton');
  const loading = document.getElementById('loading');
  const result = document.getElementById('result');

  const url = urlInput.value.trim();

  if (!url) {
    alert('Please enter a URL');
    return;
  }

  // Show loading
  checkButton.disabled = true;
  loading.style.display = 'block';
  result.style.display = 'none';

  try {
    const resultData = await checkPhishing(url);
    displayResult(resultData);
  } catch (error) {
    displayResult({ error: 'Failed to check URL' });
  } finally {
    checkButton.disabled = false;
    loading.style.display = 'none';
  }
});

// Initialize popup
document.addEventListener('DOMContentLoaded', () => {
  updateStatus();
});