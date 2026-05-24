# 🚀 Complete Deployment Guide - Vercel + Render + MongoDB

This guide explains how to deploy the **Phishing Detection System** using:
- **Frontend**: Vercel (static HTML/CSS/JS)
- **Backend**: Render (Spring Boot + Python FastAPI)
- **Database**: MongoDB Atlas (free)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User (Browser)                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓
        ┌────────────────────────┐
        │  Frontend (Vercel)     │
        │  index.html            │
        │  CSS + JavaScript      │
        └────────────┬───────────┘
                     │ HTTP/REST
                     ↓
    ┌────────────────────────────────────┐
    │  Backend (Render)                  │
    │  Spring Boot                       │
    │  /api/v1/check                     │
    └────────────┬───────────────────────┘
                 │
         ┌───────┴───────┐
         ↓               ↓
    ┌──────────┐   ┌──────────────┐
    │Brain API │   │   MongoDB    │
    │(Python)  │   │   Atlas      │
    │Port 8000 │   │   (Cloud)    │
    └──────────┘   └──────────────┘
```

---

## ✅ Deployment Checklist

### Phase 1: Database Setup

- [ ] Create MongoDB Atlas account (free)
- [ ] Create free cluster
- [ ] Create database user
- [ ] Get connection string
- [ ] Whitelist all IPs

### Phase 2: Backend Deployment (Render)

- [ ] Deploy Brain API (Python)
- [ ] Deploy Orchestrator (Java)
- [ ] Configure environment variables
- [ ] Verify both services are online

### Phase 3: Frontend Deployment (Vercel)

- [ ] Push frontend folder to GitHub
- [ ] Connect Vercel to GitHub
- [ ] Configure environment variables
- [ ] Verify frontend is live

---

## 📋 Step-by-Step

### STEP 1: MongoDB Atlas Setup (5 minutes)

1. Go to [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
2. Sign up (free)
3. Create project → Create deployment (FREE tier)
4. Choose AWS, any region
5. Create database user:
   - Username: `akcreate888_db_user`
   - Password: `GGo1sDm0lqu3oBTH`
6. Network Access → Allow all IPs (for testing)
7. Get connection string:
   ```
   mongodb+srv://akcreate888_db_user:GGo1sDm0lqu3oBTH@cluster101.aq9wgtm.mongodb.net/phishing_detection?retryWrites=true&w=majority
   ```

**Save this! You'll need it next.**

---

### STEP 2: Deploy Backend to Render (20 minutes)

#### Option A: Simple Method (Recommended)

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Configure:

**For Brain API:**
```
Name: brain-api
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Root Directory: brain-api
```

**For Orchestrator:**
```
Name: orchestrator-service
Build Command: [leave empty]
Start Command: [leave empty]
Root Directory: orchestrator-service
Dockerfile: ./orchestrator-service/Dockerfile
```

6. Add Environment Variables (Orchestrator only):
```
MONGODB_URI=mongodb+srv://akcreate888_db_user:GGo1sDm0lqu3oBTH@cluster101.aq9wgtm.mongodb.net/phishing_detection?retryWrites=true&w=majority
BRAIN_API_URL=https://brain-api-XXXX.onrender.com/predict
SERVER_PORT=8080
```

7. Click "Deploy"
8. Wait 10-15 minutes for both to build

**Your backend URLs:**
```
Brain API: https://brain-api-XXXX.onrender.com
Orchestrator: https://orchestrator-XXXX.onrender.com
```

---

### STEP 3: Deploy Frontend to Vercel (10 minutes)

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Import your repository
5. Configure:
   ```
   Root Directory: frontend
   Framework: Other (static)
   ```
6. Add Environment Variables:
   ```
   REACT_APP_API_URL=https://orchestrator-XXXX.onrender.com
   ```
   (Use actual Render URL from Step 2)

7. Click "Deploy"
8. Wait 2-3 minutes

**Your frontend URL:**
```
https://phishing-detector-frontend.vercel.app
```

---

## 🧪 Testing

### Test 1: Frontend Loads
```
Open: https://phishing-detector-frontend.vercel.app
Expected: Should see the phishing detector form
```

### Test 2: API Health
```bash
curl https://orchestrator-XXXX.onrender.com/api/v1/health
Expected: {"status":"ok"}
```

### Test 3: Full Check
```bash
curl -X POST https://orchestrator-XXXX.onrender.com/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
Expected: {"isPhishing":false,"confidence":0.95,"explanation":"..."}
```

### Test 4: Frontend to Backend
1. Open frontend URL
2. Enter URL: `https://example.com`
3. Click "Check for Phishing"
4. Should show result with confidence score

---

## 🔧 Environment Variables Summary

### Vercel (Frontend)
```
REACT_APP_API_URL=https://orchestrator-XXXX.onrender.com
```

### Render Orchestrator (Backend)
```
MONGODB_URI=mongodb+srv://...
BRAIN_API_URL=https://brain-api-XXXX.onrender.com/predict
SERVER_PORT=8080
```

### Render Brain API (Python)
```
[No env vars needed]
```

### MongoDB Atlas
```
Already configured at: cluster101.aq9wgtm.mongodb.net
```

---

## 📊 Deployment Summary

| Component | Platform | Status | URL |
|-----------|----------|--------|-----|
| Frontend | Vercel | 🟢 Online | phishing-detector-frontend.vercel.app |
| Brain API | Render | 🟢 Online | brain-api-XXXX.onrender.com |
| Orchestrator | Render | 🟢 Online | orchestrator-XXXX.onrender.com |
| MongoDB | MongoDB Atlas | 🟢 Online | cluster101.aq9wgtm.mongodb.net |

---

## 🚨 Troubleshooting

### Frontend shows error
- Check backend URL in Vercel environment variables
- Make sure Render services are online
- Check browser console (F12)

### Backend won't start
- Check logs in Render dashboard
- Verify MongoDB connection string
- Ensure Brain API URL is correct

### Services can't communicate
- Verify environment variables
- Check firewall/network settings
- MongoDB: allow all IPs in Network Access

### 502 Bad Gateway
- Wait a few minutes for Render build to complete
- Refresh page
- Check service logs

---

## 💡 Tips

1. **Save URLs**: After deployment, note down all service URLs
2. **Monitor costs**: All services use free tier (no credit card charged)
3. **Auto-deploy**: Every GitHub push automatically redeploys
4. **Team sharing**: Share Vercel link with team - backend handles everything

---

## 📞 Support

**Issue?** Check these in order:
1. Read service logs (Vercel/Render dashboard)
2. Test each component separately
3. Verify environment variables
4. Check MongoDB connection

---

## 🎉 Success Indicators

✅ When everything works:
- Frontend loads at Vercel URL
- Health check returns 200 OK
- API returns results with confidence score
- Data is stored in MongoDB

---

**Your deployment is ready!** 🚀
