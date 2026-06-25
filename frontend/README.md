# 🔍 Phishing Detection - Frontend (Vercel)

This is the frontend for the Phishing Detection System. It's a simple static HTML/CSS/JS application that connects to the backend API.

## 📂 Structure

```
frontend/
├── index.html          # Main application
├── package.json        # Project metadata
├── vercel.json         # Vercel deployment config
├── .env.example        # Environment variables template
└── README.md           # This file
```

## 🚀 Local Development

### Run Locally

**Option 1: Using Python**
```bash
cd frontend
python -m http.server 3000
# Visit: http://localhost:3000
```

**Option 2: Using Node.js**
```bash
cd frontend
npx http-server -p 3000
# Visit: http://localhost:3000
```

### Configure Backend URL

For local testing, the frontend expects the backend at:
```
http://localhost:8080
```

If backend is on different port/URL, update in `index.html`:
```javascript
const API_BASE_URL = 'http://your-backend-url:port';
```

## 🌐 Deploy to Vercel

### Prerequisites
- GitHub account with this repo
- Vercel account (free)

### Step 1: Push to GitHub

```bash
# Make sure you're in the repo root
git add frontend/
git commit -m "Add frontend for Vercel deployment"
git push origin main
```

### Step 2: Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Select your GitHub repo
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework**: "Other" (static site)
5. Click "Deploy"

### Step 3: Add Environment Variable

1. In Vercel dashboard, go to project settings
2. Go to "Environment Variables"
3. Add:
   ```
   REACT_APP_API_URL = https://orchestrator-XXXX.onrender.com
   ```
   (Replace with your actual Render URL)

4. Redeploy

### Step 4: Your Live Frontend

```
https://phishing-detector-frontend.vercel.app
```

## 📋 Environment Variables

| Variable | Value | When |
|----------|-------|------|
| `REACT_APP_API_URL` | `http://localhost:8080` | Local dev |
| `REACT_APP_API_URL` | `https://orchestrator-XXXX.onrender.com` | Production (Vercel) |

## 🔗 API Integration

Frontend calls this endpoint:
```
POST {API_URL}/api/v1/check
Content-Type: application/json

{
  "url": "https://example.com"
}
```

Expected response:
```json
{
  "isPhishing": false,
  "confidence": 0.95,
  "explanation": "URL appears safe based on analysis"
}
```

## 🐛 Troubleshooting

### "Network error. Backend not responding"
- Make sure backend is running
- Check `REACT_APP_API_URL` is correct
- Check backend allows CORS from your frontend URL

### Frontend loads but buttons don't work
- Check browser console for errors (F12)
- Verify API URL in environment variables
- Check backend is deployed and online

### CORS Errors
The backend needs to allow requests from your Vercel URL. Check Spring Boot CORS config:
```yaml
# In orchestrator-service/src/main/resources/application.yml
cors:
  allowed-origins: https://phishing-detector-frontend.vercel.app
```

## 📚 Stack

- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript (Vanilla)** - Frontend logic
- **Vercel** - Hosting

## 🔄 Deployment Flow

```
Frontend (Vercel)
     ↓ (calls API)
Backend (Render)
     ↓ (calls ML)
Brain API (Render)
     ↓ (uses)
MongoDB Atlas
```

## 📞 Support

For issues:
1. Check browser console (F12 → Console tab)
2. Check Render backend logs
3. Verify environment variables
4. Check MongoDB connection

---

**Frontend is ready to deploy to Vercel!** 🎉
