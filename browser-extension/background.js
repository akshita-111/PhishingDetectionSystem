// Background script for phishing detection

// Deployed orchestrator backend URL
const BACKEND_URL = 'https://orchestrator-services.onrender.com';
const API_URL = `${BACKEND_URL}/api/v1/check`;

// Check if URL is phishing
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
    return null;
  }
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