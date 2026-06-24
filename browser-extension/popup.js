// Popup script

// Define your backend URLs here once deployed
const ORCHESTRATOR_URL = 'https://akshita118-phishing-orchestrator.hf.space';
const ORCHESTRATOR_API_URL = `${ORCHESTRATOR_URL}/api/v1/check`;
const ORCHESTRATOR_HEALTH_URL = `${ORCHESTRATOR_URL}/api/v1/health`;
const BRAIN_API_URL = 'https://akshita118-brain-api.hf.space/predict';

// Check service health
async function checkServiceHealth() {
  try {
    const response = await fetch(ORCHESTRATOR_HEALTH_URL);
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

// Check phishing for a URL with fallback
async function checkPhishing(url) {
  // Try orchestrator service first
  try {
    const response = await fetch(ORCHESTRATOR_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url })
    });

    if (response.ok) {
      const data = await response.json();
      return data;
    }
  } catch (error) {
    console.log('Orchestrator service unavailable, trying brain API directly');
  }

  // Fallback to brain API directly
  try {
    const response = await fetch(BRAIN_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url })
    });

    if (response.ok) {
      const data = await response.json();
      // Convert brain API response to match orchestrator format
      return {
        isPhishing: data.is_phishing,
        confidence: data.confidence,
        explanation: data.explanation
      };
    }
  } catch (error) {
    console.log('Brain API also unavailable');
  }

  return { error: 'Both services are currently unavailable' };
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