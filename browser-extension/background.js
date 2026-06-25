// Background script for phishing detection

// Load configuration
const ORCHESTRATOR_URL = 'https://orchestrator-services-fy67.onrender.com';
const ORCHESTRATOR_API_URL = `${ORCHESTRATOR_URL}/api/v1/check`;
const BRAIN_API_URL = 'https://brain-api-3pru.onrender.com/predict';

// Check if URL is phishing with fallback
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

  return null;
}

// Show notification
function showPhishingNotification(url, confidence) {
  const confidencePercent = Math.round(confidence * 100);

  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icons/icon48.png',
    title: '⚠️ Phishing Alert!',
    message: `This website (${url}) appears to be phishing with ${confidencePercent}% confidence.`,
    buttons: [
      { title: 'Close Tab' },
      { title: 'Ignore' }
    ],
    requireInteraction: true
  });
}

// Handle notification button clicks
chrome.notifications.onButtonClicked.addListener((notificationId, buttonIndex) => {
  if (buttonIndex === 0) {
    // Close tab - find the active tab and close it
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.remove(tabs[0].id);
      }
    });
  }
  // Button 1 (Ignore) just closes the notification
  chrome.notifications.clear(notificationId);
});

// Listen for tab updates
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  // Only check when the page has finished loading
  if (changeInfo.status === 'complete' && tab.url) {
    // Skip non-HTTP URLs (like chrome://, file://, etc.)
    if (!tab.url.startsWith('http://') && !tab.url.startsWith('https://')) {
      return;
    }

    console.log('Checking URL:', tab.url);

    const result = await checkPhishing(tab.url);

    if (result && result.isPhishing) {
      showPhishingNotification(tab.url, result.confidence);
    }
  }
});

// Handle extension installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('Phishing Detection Extension installed');
});