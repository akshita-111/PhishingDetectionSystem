# Phishing Detection Browser Extension

This browser extension detects phishing websites and alerts users with notifications and popups.

## Features

- **Automatic Detection**: Monitors visited websites and checks for phishing
- **Browser Notifications**: Shows alerts when phishing sites are detected
- **Extension Popup**: Manual URL checking and service status
- **Real-time Analysis**: Uses machine learning model via backend API

## Installation

### Chrome
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked" and select the `browser-extension` folder
4. The extension should now be installed

### Firefox
1. Open Firefox and go to `about:debugging`
2. Click "This Firefox" in the left sidebar
3. Click "Load Temporary Add-on"
4. Select the `manifest.json` file in the `browser-extension` folder

## Setup

1. Make sure your backend services are running:
   - Brain API (Python FastAPI) on `http://localhost:8000`
   - Orchestrator Service (Spring Boot) on `http://localhost:8080`

2. The extension will automatically check URLs when you visit websites

## Usage

### Automatic Detection
- The extension automatically checks every website you visit
- If a phishing site is detected, you'll see a browser notification
- Click "Close Tab" to close the suspicious tab, or "Ignore" to dismiss

### Manual Checking
- Click the extension icon in your browser toolbar
- Enter a URL in the popup and click "Check URL"
- View the analysis results directly in the popup

## Icons

The extension requires icon files in the `icons/` directory:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

You can create these using any image editor or online icon generator. Use a shield or warning symbol to represent security/phishing detection.

## Permissions

The extension requires the following permissions:
- `tabs`: To monitor tab changes and URLs
- `activeTab`: To interact with the current tab
- `notifications`: To show phishing alerts
- `storage`: To store extension settings
- `http://localhost:8080/*`: To communicate with the backend API

## Development

To modify the extension:
1. Edit the source files
2. Reload the extension in `chrome://extensions/` (Chrome) or `about:debugging` (Firefox)
3. Test the changes

## Troubleshooting

- **Service Offline**: Make sure both backend services are running
- **No Notifications**: Check that browser notifications are enabled
- **Extension Not Loading**: Ensure all files are in the correct locations

## Security Note

This extension communicates with a local backend service. In production, consider using HTTPS and proper authentication for the API endpoints.