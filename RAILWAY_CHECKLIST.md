# 🚀 Railway Deployment Checklist

Quick reference for deploying your phishing detector system.

## Before Deployment

- [ ] All code pushed to GitHub
- [ ] MongoDB Atlas account created
- [ ] MongoDB cluster created (free tier)
- [ ] MongoDB connection string copied
- [ ] Railway account created

## Step-by-Step

### 1. MongoDB Setup (5 min)
- [ ] Create cluster on [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
- [ ] Get connection string
- [ ] Allow all IPs (Network Access)
- [ ] Copy connection string (save for later)

### 2. Push to GitHub (2 min)
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 3. Railway Setup (15 min)

#### Create Project
- [ ] Go to [railway.app](https://railway.app)
- [ ] Sign up with GitHub
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose phishing-detection repo
- [ ] Click "Deploy"

#### Brain API Configuration
- [ ] Find "Brain API" service in Railway
- [ ] Set Dockerfile: `./brain-api/Dockerfile`
- [ ] Set Root Directory: `./brain-api`
- [ ] Add variable: `PYTHONUNBUFFERED=1`
- [ ] Wait for build to complete ✅

#### Orchestrator Configuration
- [ ] Find "Orchestrator Service" in Railway
- [ ] Set Dockerfile: `./orchestrator-service/Dockerfile`
- [ ] Set Root Directory: `./orchestrator-service`
- [ ] Add these variables:
  ```
  MONGODB_URI=[paste your connection string]
  BRAIN_API_URL=http://brain-api:8000/predict
  SERVER_PORT=8080
  SPRING_DATA_MONGODB_AUTO_INDEX_CREATION=true
  ```
- [ ] Wait for build to complete ✅

### 4. Verify Deployment (5 min)
- [ ] Both services show ✅ status
- [ ] Check Brain API logs (no errors)
- [ ] Check Orchestrator logs (no errors)

### 5. Test Live App (5 min)
- [ ] Open `https://orchestrator-service.railway.app`
- [ ] Test URL check functionality
- [ ] Test API: `curl -X POST https://orchestrator-service.railway.app/api/v1/check -H "Content-Type: application/json" -d '{"url": "https://example.com"}'`
- [ ] Expected response: `{"isPhishing": false, "confidence": ...}`

### 6. Share with Team (3 min)
- [ ] Copy live URL: `https://orchestrator-service.railway.app`
- [ ] Share in team chat
- [ ] Invite team members in Railway (Settings → Members)

## Your Live URLs

Once deployed, your team can access:

```
🌐 Frontend:     https://orchestrator-service.railway.app
📡 API:          https://orchestrator-service.railway.app/api/v1/check
📚 Docs:         https://brain-api.railway.app/docs
🏥 Health:       https://orchestrator-service.railway.app/api/v1/health
```

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check logs, look for syntax errors |
| Services won't connect | Verify MongoDB connection string |
| 502 Bad Gateway | Wait a few minutes, refresh page |
| Port error | Railway assigns ports automatically |

## Auto-Deploy On Push

```bash
# Any team member can push updates
git push origin main

# Railway automatically:
# ✅ Detects changes
# ✅ Rebuilds services
# ✅ Deploys new version
# ✅ No downtime!
```

## Environment Variables Reference

| Variable | Value | Where |
|----------|-------|-------|
| `MONGODB_URI` | `mongodb+srv://...` | Orchestrator |
| `BRAIN_API_URL` | `http://brain-api.railway.internal:8000/predict` | Orchestrator |
| `SERVER_PORT` | `8080` | Orchestrator |
| `PYTHONUNBUFFERED` | `1` | Brain API |

## Cost

- **Railway**: $5/month credit (free tier)
- **MongoDB Atlas**: FREE forever
- **Total**: FREE for small team projects

---

**Total Time to Deploy: ~30 minutes** ⏱️

Need help? See `DEPLOY_RAILWAY_GUIDE.md` for detailed steps.
