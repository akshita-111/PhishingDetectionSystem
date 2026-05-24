# 🚀 Deploy to Railway - Step-by-Step Guide

Deploy all 3 services together on Railway (like Vercel for backend).

## 📋 Prerequisites

- GitHub account with your repo pushed
- MongoDB Atlas account (free)
- Railway account

---

## ✅ Step 1: Create MongoDB Atlas Cluster (FREE)

This is where your data lives.

### 1.1 Sign up for MongoDB Atlas
- Go to [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
- Click "Sign Up"
- Create free account

### 1.2 Create Free Cluster
1. Click "Create a Deployment"
2. Select **"FREE"** tier
3. Choose region (any region is fine)
4. Click "Create Deployment"

### 1.3 Get Connection String
1. Click "Database" → "Databases"
2. Find your cluster → Click "Connect"
3. Choose "Drivers" (not application)
4. Copy connection string: 
   ```
   mongodb+srv://USERNAME:PASSWORD@cluster0.xxxxx.mongodb.net/phishing_detection?retryWrites=true&w=majority
   ```
5. Replace `USERNAME` and `PASSWORD` with your credentials
6. **Save this for later!**

### 1.4 Allow All IPs (for testing)
1. Go to "Security" → "Network Access"
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere"
4. Confirm

---

## ✅ Step 2: Prepare GitHub Repository

Make sure all files are ready.

```bash
# Navigate to your project
cd /path/to/phishing-detection

# Check git status
git status

# Add all files
git add .

# Commit
git commit -m "Prepare for Railway deployment"

# Push to GitHub
git push origin main
```

---

## ✅ Step 3: Create Railway Project

### 3.1 Sign Up for Railway
- Go to [railway.app](https://railway.app)
- Click "Sign Up"
- Select "GitHub" (easiest)
- Authorize Railway to access your GitHub

### 3.2 Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Find and select `phishing-detection` repository
4. Click "Deploy"

Railway will start detecting services...

---

## ✅ Step 4: Configure Brain API Service

Railway should auto-detect or you can add manually.

### 4.1 In Railway Dashboard
1. Click **"Brain API"** service
2. Go to **"Settings"**
3. Set:
   - **Dockerfile**: `./brain-api/Dockerfile`
   - **Root Directory**: `./brain-api`

### 4.2 Add Variables
1. Click **"Variables"** tab
2. Add:
   ```
   PYTHONUNBUFFERED=1
   ```

### 4.3 Confirm
- Port should be: `8000`
- Status should show: ✅ Building...

---

## ✅ Step 5: Configure Orchestrator Service

### 5.1 In Railway Dashboard
1. Click **"Orchestrator Service"** service
2. Go to **"Settings"**
3. Set:
   - **Dockerfile**: `./orchestrator-service/Dockerfile`
   - **Root Directory**: `./orchestrator-service`

### 5.2 Add Environment Variables
1. Click **"Variables"** tab
2. Add these variables:

```
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@cluster0.xxxxx.mongodb.net/phishing_detection?retryWrites=true&w=majority
```
(Paste your MongoDB Atlas connection string from Step 1.3)

```
BRAIN_API_URL=http://brain-api:8000/predict
```

```
SERVER_PORT=8080
```

```
SPRING_DATA_MONGODB_AUTO_INDEX_CREATION=true
```

### 5.3 Confirm
- Port should be: `8080`
- Status should show: ✅ Building...

---

## ✅ Step 6: Wait for Deployment

Railway will:
1. Pull your code from GitHub
2. Build Brain API (Python) - ~2-3 minutes
3. Build Orchestrator (Java) - ~5-10 minutes
4. Start both services
5. They automatically discover each other

**Watch the logs** - you should see:
```
✅ Brain API ready on port 8000
✅ Orchestrator Service ready on port 8080
✅ Connected to MongoDB
```

---

## ✅ Step 7: Get Your Live URLs

Once deployed, find your URLs:

### 7.1 In Railway Dashboard
1. Click "Orchestrator Service"
2. Look for "Deployments" section
3. You'll see:
   ```
   Deployments
   orchestrator-service.railway.app ← CLICK THIS
   ```

### 7.2 Your Live Services
- **Frontend & API**: `https://orchestrator-service.railway.app`
- **Brain API**: `https://brain-api.railway.app/docs`
- **Health Check**: `https://orchestrator-service.railway.app/api/v1/health`

---

## ✅ Step 8: Test Your Deployment

### 8.1 Test API
```bash
curl -X POST https://orchestrator-service.railway.app/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Expected response:
```json
{
  "isPhishing": false,
  "confidence": 0.85,
  "explanation": "URL appears safe"
}
```

### 8.2 Test in Browser
Open: `https://orchestrator-service.railway.app`

You should see your phishing detector UI!

---

## ✅ Step 9: Share with Your Team

### 9.1 Invite Team Members
1. In Railway Dashboard
2. Click "Settings"
3. Go to "Members"
4. Click "Invite"
5. Enter team member emails

### 9.2 Team Members Can See
- Live deployments
- Logs in real-time
- Environment variables
- Deployment history

### 9.3 Everyone Can Access Live App
```
https://orchestrator-service.railway.app ← Share this URL!
```

---

## ✅ Step 10: Auto-Deploy on Code Push

Every time someone pushes to GitHub, Railway automatically redeploys!

```bash
# Team member makes changes
git add .
git commit -m "Fix bug in phishing detection"
git push origin main

# Railway automatically:
# 1. Detects the push
# 2. Rebuilds services
# 3. Deploys new version
# 4. No downtime!
```

---

## 🔧 Troubleshooting

### Problem: Services won't start
**Solution:**
1. Check Railway logs (click service → "Logs")
2. Look for error messages
3. Make sure MONGODB_URI is correct

### Problem: Brain API can't connect to MongoDB
**Solution:**
1. Verify MongoDB Atlas IP whitelist (Step 1.4)
2. Check connection string has right username/password
3. Check database name is `phishing_detection`

### Problem: Orchestrator can't reach Brain API
**Solution:**
1. Verify `BRAIN_API_URL=http://brain-api.railway.internal:8000/predict`
2. Check Brain API service is running (see logs)

### Problem: Port already in use
**Solution:**
- Railway automatically assigns ports, no need to worry

### Problem: 502 Bad Gateway
**Solution:**
1. Wait a few minutes for deployment to complete
2. Refresh browser
3. Check service logs

---

## 📊 Monitoring

In Railway Dashboard you can see:

- **Build Logs** - what happens during deployment
- **Runtime Logs** - errors and info from running services
- **Metrics** - CPU, memory, bandwidth usage
- **Deployments** - history of all deployments
- **Variables** - all environment variables

---

## 💰 Cost

| Item | Free Tier | Cost |
|------|-----------|------|
| Railway | $5/month credit | Usually free for small projects |
| MongoDB Atlas | Free tier (512MB) | FREE forever for testing |
| **Total** | | **FREE!** |

---

## 🎉 You're Done!

Your phishing detector is now live on:
```
https://orchestrator-service.railway.app
```

### Next Steps:
- ✅ Share with your team
- ✅ Test thoroughly
- ✅ Collect feedback
- ✅ Push improvements (auto-deploys!)

---

## 📞 Need Help?

- Railway Docs: [railway.app/docs](https://railway.app/docs)
- MongoDB Atlas: [mongodb.com/docs](https://mongodb.com/docs)
- API Docs: `https://orchestrator-service.railway.app/swagger-ui.html` (if available)

---

## Quick Reference

| Service | URL | Status |
|---------|-----|--------|
| Frontend | `https://orchestrator-service.railway.app` | 🟢 Live |
| API Endpoint | `https://orchestrator-service.railway.app/api/v1/check` | 🟢 Live |
| Brain API Docs | `https://brain-api.railway.app/docs` | 🟢 Live |
| Health Check | `https://orchestrator-service.railway.app/api/v1/health` | 🟢 Live |
| MongoDB | Internal | 🟢 Connected |
