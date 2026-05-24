# ❓ Railway Deployment FAQ & Troubleshooting

## Common Questions

### Q: Will all 3 services really work together?
**A:** Yes! They're designed to communicate:
- Users hit Orchestrator (8080)
- Orchestrator calls Brain API (8000)
- Both use MongoDB for data
- All automatic on Railway

### Q: Do I need to create MongoDB first?
**A:** Yes, before deploying:
1. Create free MongoDB Atlas cluster
2. Get connection string
3. Add to Railway environment variables

### Q: How long does deployment take?
**A:** 
- Python (Brain API): 2-3 minutes
- Java (Orchestrator): 5-10 minutes
- Total: ~10-15 minutes

### Q: Can I use a local MongoDB instead of Atlas?
**A:** Not recommended for production, but you can:
- Add MongoDB service in Railway
- Or use self-hosted MongoDB
- Just update connection string

### Q: How do I update the code after deployment?
**A:** Super easy:
```bash
git push origin main
# Railway automatically redeploys!
```

### Q: Can multiple team members access it?
**A:** Yes!
1. Invite them in Railway dashboard
2. Give them the live URL
3. They can use it immediately

### Q: Is it safe? What about data?
**A:** 
- Data stored in MongoDB Atlas (encrypted)
- URLs are checked, not stored permanently
- HTTPS enabled automatically
- Free for testing, upgrade for production security

### Q: What's the cost?
**A:**
- Railway: $5/month free credit (enough for small team)
- MongoDB: FREE forever (free tier)
- Total: FREE for testing/small projects

### Q: Can I use my own domain?
**A:** Yes, Railway supports custom domains
1. Go to Railway service settings
2. Add custom domain
3. Update DNS records

---

## Troubleshooting

### 🔴 Build Fails During Deployment

**Error:** Build failed, services won't start

**Causes:**
- Missing dependencies
- Syntax errors in code
- Java/Python version mismatch

**Solution:**
1. Check build logs in Railway
2. Look for red error messages
3. Test locally with docker-compose:
```bash
docker-compose up
```
4. Fix errors
5. Push to GitHub (auto-redeploys)

---

### 🔴 Services Can't Connect to MongoDB

**Error:** Connection refused, database error

**Solution:**
1. Verify MongoDB Atlas is running
2. Check connection string is correct
3. Verify username/password (no typos)
4. Check IP whitelist:
   - Go to MongoDB Atlas → Security → Network Access
   - Click "Add IP Address"
   - Select "Allow Access from Anywhere"
5. Add MongoDB credentials to Railway variables

---

### 🔴 Brain API Can't Connect to Orchestrator (or vice versa)

**Error:** Services won't communicate

**Solution:**
1. Use internal URL: `http://brain-api.railway.internal:8000`
2. NOT external URL like `https://brain-api.railway.app`
3. Update `BRAIN_API_URL` in Orchestrator variables

---

### 🔴 502 Bad Gateway Error

**Error:** `502 Bad Gateway` when accessing the app

**Solutions:**
1. Wait a few minutes for deployment
2. Refresh the page (Ctrl+F5)
3. Check service status in Railway
4. Check logs for errors:
   - Click service → "Logs" tab
   - Look for red error messages

---

### 🔴 Port Already in Use

**Error:** Port 8080 already in use

**Solution:**
- Railway automatically assigns ports
- You don't need to worry about this
- Check Railway dashboard for actual port

---

### 🔴 MongoDB Connection String Issues

**Error:** `MongoNetworkError` or `Invalid URI`

**Common Mistakes:**
- ❌ `mongodb://` (old format)
- ✅ `mongodb+srv://` (new format)

- ❌ Missing `@cluster`
- ✅ `mongodb+srv://user:pass@cluster.mongodb.net`

- ❌ Special characters not escaped
- ✅ Replace `@` with `%40`, `:` with `%3A`

**Solution:**
```
# Correct format:
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/phishing_detection?retryWrites=true&w=majority
```

---

### 🔴 Services Restart Constantly

**Error:** Services keep restarting, won't stay up

**Causes:**
- Out of memory
- Crash on startup
- Invalid configuration

**Solution:**
1. Check logs for error messages
2. Verify all environment variables are set
3. Test locally first
4. Check if Railway tier is sufficient

---

### 🔴 Frontend Loads but API Returns Errors

**Error:** UI works but "Check URL" button fails

**Likely Cause:**
- Frontend can load, but can't reach API
- Or API can't reach Brain API

**Solution:**
1. Check Orchestrator logs
2. Verify Brain API is running
3. Check BRAIN_API_URL variable
4. Test API directly:
```bash
curl https://orchestrator-service.railway.app/api/v1/health
```

---

### 🔴 Java Build Takes Very Long

**Note:** This is normal!
- First Java build: 10+ minutes
- Subsequent builds: 5-7 minutes
- Maven downloads dependencies

**Just wait**, don't cancel the build.

---

### 🔴 Python Dependencies Won't Install

**Error:** `pip install` fails

**Solution:**
1. Check requirements.txt for typos
2. Ensure Python 3.10 compatibility
3. Look for C compiler dependencies
4. Check Railway logs for details

---

## How to Debug

### 1. Check Logs
```
Railway Dashboard 
  → Select Service 
  → "Logs" tab 
  → Look for errors
```

### 2. Test Service Locally
```bash
docker-compose up
# Test at http://localhost:8080
```

### 3. Check Environment Variables
```
Railway Dashboard 
  → Select Service 
  → "Variables" tab 
  → Verify all variables are correct
```

### 4. Check MongoDB Connection
```bash
# From your computer (not Railway)
mongosh "mongodb+srv://user:pass@cluster.mongodb.net/phishing_detection"
# Should connect successfully
```

### 5. Test API Endpoint
```bash
curl -X GET https://orchestrator-service.railway.app/api/v1/health
# Should return 200 OK
```

---

## Performance Issues

### Slow API Responses
- Add more railway credits for better CPU
- Optimize Java application
- Check MongoDB indexes

### High Memory Usage
- Check for memory leaks in code
- Reduce number of replicas
- Optimize database queries

### Database Timeouts
- Increase MongoDB timeout settings
- Check network connection quality
- Verify MongoDB cluster is responsive

---

## When to Upgrade

| Issue | Solution |
|-------|----------|
| Runs out of credits | Buy more Railway credits |
| Too slow | Upgrade to paid Railway tier |
| Need more storage | Increase MongoDB plan |
| Need SSL/TLS | Railway provides free HTTPS |

---

## Getting Help

1. **Railway Docs**: [railway.app/docs](https://railway.app/docs)
2. **MongoDB Docs**: [mongodb.com/docs](https://mongodb.com/docs)
3. **GitHub Issues**: Document problems in repo
4. **Team Discussion**: Ask teammates

---

## Quick Reference Commands

```bash
# Local testing
docker-compose up

# Push and deploy
git add .
git commit -m "message"
git push origin main

# Check specific service logs
# (In Railway Dashboard, select service, click "Logs")

# Test API
curl -X POST https://orchestrator-service.railway.app/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## Common Environment Variable Mistakes

```bash
# ❌ WRONG
MONGODB_URI=mongodb://localhost:27017/phishing

# ✅ CORRECT
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/phishing_detection

# ❌ WRONG
BRAIN_API_URL=https://brain-api.railway.app/predict

# ✅ CORRECT
BRAIN_API_URL=http://brain-api:8000/predict
```

---

## Success Indicators

✅ When everything works:
- Both services show green status
- No errors in logs
- Can access frontend
- API returns responses
- MongoDB stores data

---

Still stuck? Check the detailed guide: `DEPLOY_RAILWAY_GUIDE.md`
