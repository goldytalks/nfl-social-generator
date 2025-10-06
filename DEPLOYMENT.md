# 🚀 Deployment Guide - NFL Social Content Generator

## Vercel Deployment (Recommended)

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Sign in with GitHub

2. **Import Repository**
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Choose: `goldytalks/nfl-social-generator`

3. **Configure Project**
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as default)
   - Build Command: (leave empty - not needed for Flask)
   - Output Directory: (leave empty)

4. **Environment Variables** (Important!)
   Click "Environment Variables" and add:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-random-string>
   DEBUG=False
   ```

   To generate a secure SECRET_KEY, run locally:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - You'll get a URL like: `nfl-social-generator-xxx.vercel.app`

6. **Test**
   - Visit your deployed URL
   - Upload the sample CSV: `data/sample_odds.csv`
   - Verify all 4 steps work correctly

---

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not installed)
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd nfl-social-generator
   vercel
   ```

   Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - What's your project's name? `nfl-social-generator`
   - In which directory is your code located? `./`

4. **Set Environment Variables**
   ```bash
   vercel env add SECRET_KEY
   # Paste your secret key when prompted

   vercel env add FLASK_ENV
   # Type: production

   vercel env add DEBUG
   # Type: False
   ```

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

---

### Option 3: Automatic Deployments (Recommended After Initial Setup)

Once you've completed Option 1 or 2:

1. **Connect GitHub** (if using Dashboard method)
   - Vercel should auto-detect your GitHub repo
   - Enable automatic deployments

2. **How it works:**
   - Every push to `main` branch → Automatic deployment
   - Every pull request → Preview deployment
   - Vercel comments on commits with deployment URL

3. **Update your project:**
   ```bash
   git add .
   git commit -m "feat: your changes"
   git push origin main
   ```

   Vercel will automatically deploy in ~2 minutes!

---

## Post-Deployment Checklist

### ✅ Verify Deployment

1. **Homepage loads** - Visit your Vercel URL
2. **CSV Upload works** - Upload `data/sample_odds.csv`
3. **Analysis works** - Click "Analyze Movers"
4. **Generation works** - Click "Generate Tweets"
5. **Export works** - Click "Export to JSON"

### ✅ Performance Check

1. **Cold Start Time** - First request may take 2-3 seconds (normal for serverless)
2. **Subsequent Requests** - Should be < 1 second
3. **File Upload** - Should handle up to 10MB CSVs

### ✅ Update Documentation

1. **Update PROJECT_BRAIN.md**
   - Add deployment URL
   - Update "Current Status" section
   - Log deployment date in Change Log

2. **Update README.md**
   - Add live demo link
   - Update deployment status

---

## Vercel Settings

### Recommended Settings

**Project Settings:**
- Build Command: (empty)
- Output Directory: (empty)
- Install Command: `pip install -r requirements.txt`
- Development Command: `python app.py`

**Serverless Function Settings:**
- Region: Choose closest to your users (e.g., `iad1` for US East)
- Function Memory: 1024 MB (default)
- Function Timeout: 10s (default is fine)

**Domain Settings:**
- Vercel provides free subdomain: `*.vercel.app`
- Can add custom domain in settings

---

## Environment Variables Reference

| Variable | Development | Production | Description |
|----------|------------|------------|-------------|
| `FLASK_ENV` | development | production | Flask environment |
| `DEBUG` | True | False | Debug mode |
| `SECRET_KEY` | dev-key | random-string | Flask secret key |
| `UPLOAD_FOLDER` | data/uploads | data/uploads | Upload directory |
| `EXPORT_FOLDER` | data/exports | data/exports | Export directory |

---

## Troubleshooting

### Issue: Build Fails

**Error:** `ModuleNotFoundError`
- **Fix:** Check `requirements.txt` has all dependencies
- **Run:** `pip freeze > requirements.txt` locally

**Error:** `No Python version specified`
- **Fix:** Vercel auto-detects Python. Ensure `app.py` exists in root.

---

### Issue: 500 Internal Server Error

**Check Vercel Logs:**
1. Go to Vercel Dashboard
2. Click your project
3. Click "Deployments"
4. Click latest deployment
5. Click "Functions" tab
6. View error logs

**Common Causes:**
- Missing environment variables
- Incorrect SECRET_KEY
- File permission issues (uploads folder)

---

### Issue: Uploads Not Working

**Cause:** Serverless functions use `/tmp` for temporary storage

**Fix (Phase 2):**
- Use cloud storage (AWS S3, Google Cloud Storage)
- Or use Vercel Blob storage
- Or keep uploads in memory (current approach)

**Current Workaround:**
- Files are stored temporarily during request
- Exports are returned immediately, not stored persistently

---

### Issue: Slow Performance

**Cold Starts:**
- First request after inactivity = 2-3 seconds (normal)
- Happens on Vercel free tier
- Solution: Upgrade to Pro for always-warm instances

**Large CSV Processing:**
- Files > 5MB may take longer
- Vercel timeout is 10 seconds on free tier
- Solution: Upgrade to Pro for 60s timeout

---

## Monitoring & Analytics

### Vercel Analytics (Built-in)

1. **View Analytics:**
   - Go to Vercel Dashboard
   - Click "Analytics"
   - See: Page views, unique visitors, top pages

2. **Function Logs:**
   - See all function invocations
   - Error rates
   - Execution time

### Add Custom Logging (Phase 3)

Future enhancement:
- Log uploads, generations, exports
- Track most popular markets
- Monitor error rates
- User analytics

---

## Updating the Deployment

### Quick Updates

```bash
# Make changes locally
git add .
git commit -m "fix: your fix description"
git push origin main

# Vercel auto-deploys in ~2 minutes
```

### Check Deployment Status

```bash
vercel ls
# Shows all deployments

vercel inspect <deployment-url>
# Shows deployment details
```

### Rollback if Needed

1. Go to Vercel Dashboard
2. Click "Deployments"
3. Find previous working deployment
4. Click "..." → "Promote to Production"

---

## Security Considerations

### Production Security Checklist

- [x] SECRET_KEY is random and secure (not 'dev-secret-key')
- [x] DEBUG=False in production
- [x] .env file is gitignored (secrets not in repo)
- [ ] Add rate limiting (Phase 2)
- [ ] Add user authentication (Phase 2)
- [ ] Validate file uploads strictly
- [ ] Sanitize all user inputs

### Environment Variable Security

**Never commit:**
- SECRET_KEY
- API keys
- Database credentials

**Use Vercel Environment Variables** for all secrets!

---

## Cost & Limits (Vercel Free Tier)

### Free Tier Includes:
- Unlimited projects
- Unlimited deployments
- 100 GB bandwidth/month
- Serverless Function Executions: 100 GB-hours
- Function Duration: 10 seconds max
- Function Memory: 1024 MB

### When You'll Need Pro ($20/mo):
- > 100 GB bandwidth usage
- Need > 10s function timeouts
- Want always-warm instances (no cold starts)
- Need team collaboration features

**For this MVP:** Free tier is more than enough!

---

## Continuous Integration

### GitHub Actions (Future)

Can add automated testing before deployment:

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

---

## Support

### Issues?

1. Check Vercel logs first
2. Review this deployment guide
3. Check PROJECT_BRAIN.md for known issues
4. Create GitHub issue with:
   - Error message
   - Vercel deployment URL
   - Steps to reproduce

---

**Deployment Date:** TBD
**Deployed By:** Jacob G
**Deployment URL:** TBD (add after deployment)
**GitHub:** https://github.com/goldytalks/nfl-social-generator

---

*Keep this document updated with any deployment changes or issues encountered.*
