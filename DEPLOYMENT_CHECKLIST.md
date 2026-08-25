# 🚀 DEPLOYMENT CHECKLIST

Use this checklist to ensure everything is set up correctly before going live.

---

## ✅ PHASE 1: LOCAL SETUP (Development)

- [ ] **Supabase Project Created**
  - [ ] Project name: `mileage-tracker`
  - [ ] Region selected (Singapore recommended for India)
  - [ ] Password saved securely

- [ ] **Database Tables Created**
  - [ ] Ran `database_schema.sql` in Supabase SQL Editor
  - [ ] Tables visible in Supabase → Tables view:
    - [ ] `users`
    - [ ] `vehicles`
    - [ ] `fuel_records`
    - [ ] `imports`

- [ ] **Supabase Credentials Retrieved**
  - [ ] Copied Project URL from Settings → API
  - [ ] Copied anon (public) key from Settings → API
  - [ ] Pasted both into `.env` file
  - [ ] `.env` is in `.gitignore` (DON'T COMMIT!)

- [ ] **Local Environment Setup**
  - [ ] Python 3.8+ installed
  - [ ] `pip install -r requirements.txt` completed
  - [ ] All dependencies installed without errors

- [ ] **Local Testing**
  - [ ] `streamlit run app.py` runs without errors
  - [ ] App opens at http://localhost:8501
  - [ ] Can sign up with test account
  - [ ] Can add vehicle
  - [ ] Can add fuel entry
  - [ ] Mileage calculated correctly
  - [ ] Can view dashboard & charts
  - [ ] Can switch between vehicles (if added 2+)

---

## ✅ PHASE 2: GITHUB SETUP

- [ ] **Repository Created**
  - [ ] GitHub repository created: `mileage-tracker`
  - [ ] Repository is PUBLIC (for easy sharing)

- [ ] **Code Pushed to GitHub**
  - [ ] `.gitignore` created (excludes .env)
  - [ ] Files committed and pushed:
    - [ ] `app.py`
    - [ ] `requirements.txt`
    - [ ] `database_schema.sql`
    - [ ] `.env.example`
    - [ ] `.gitignore`
    - [ ] `.streamlit/config.toml`
    - [ ] `README.md`
    - [ ] `SETUP_GUIDE.md`
    - [ ] `DEPLOYMENT_CHECKLIST.md` (this file)
  - [ ] `.env` file NOT committed (verify with `git status`)

- [ ] **GitHub Actions Workflow Setup**
  - [ ] Created `.github/workflows/keep-alive.yml`
  - [ ] Replaced `https://your-project-id.supabase.co` with actual URL
  - [ ] Pushed to GitHub

- [ ] **GitHub Secrets Added**
  - [ ] Go to GitHub → Settings → Secrets and variables → Actions
  - [ ] Added `SUPABASE_URL` (your project URL)
  - [ ] Added `SUPABASE_KEY` (your anon key)

---

## ✅ PHASE 3: STREAMLIT CLOUD DEPLOYMENT

- [ ] **Streamlit Account Created**
  - [ ] Signed up at https://streamlit.io/cloud
  - [ ] Linked GitHub account

- [ ] **App Deployed**
  - [ ] Clicked "New app" in Streamlit Cloud
  - [ ] Selected repository: `mileage-tracker`
  - [ ] Selected branch: `main`
  - [ ] Set main file path: `app.py`
  - [ ] Clicked "Deploy"
  - [ ] Waited for deployment to complete (~2 minutes)
  - [ ] Got public URL: `https://username-mileage-tracker.streamlit.app`

- [ ] **Streamlit Cloud Secrets Added**
  - [ ] Clicked "..." menu → Settings (in deployed app)
  - [ ] Went to "Secrets" section
  - [ ] Added secrets:
    ```
    SUPABASE_URL = "https://xxx.supabase.co"
    SUPABASE_KEY = "your-anon-key-here"
    ```
  - [ ] Saved
  - [ ] Clicked "Reboot app" or waited for auto-reboot

- [ ] **Test Deployed App**
  - [ ] Opened public URL
  - [ ] Can sign up
  - [ ] Can login
  - [ ] Can add vehicle
  - [ ] Can add fuel entry
  - [ ] Can view dashboard
  - [ ] No errors in console (bottom right)

---

## ✅ PHASE 4: GITHUB ACTIONS SETUP

- [ ] **Workflow File Present**
  - [ ] `.github/workflows/keep-alive.yml` exists in repo
  - [ ] File contains correct Supabase URL (not the placeholder)

- [ ] **GitHub Actions Enabled**
  - [ ] Go to GitHub → Actions tab
  - [ ] "Supabase Keep-Alive" workflow visible
  - [ ] Workflow status: "Active"

- [ ] **Test Keep-Alive Workflow**
  - [ ] Manually trigger workflow:
    - [ ] Go to Actions → Select "Supabase Keep-Alive"
    - [ ] Click "Run workflow" → "Run workflow"
    - [ ] Wait for execution (should complete in <1 minute)
    - [ ] Status shows green checkmark ✅

- [ ] **Verify 24/7 Uptime**
  - [ ] Workflow runs every 5 minutes automatically
  - [ ] Supabase project will NOT pause after 7 days
  - [ ] Check Actions tab occasionally to ensure no failures

---

## ✅ PHASE 5: SHARING & TESTING

- [ ] **Share with Friends**
  - [ ] Copied app URL: `https://username-mileage-tracker.streamlit.app`
  - [ ] Shared via:
    - [ ] WhatsApp message
    - [ ] Email
    - [ ] LinkedIn
    - [ ] GitHub repository link

- [ ] **Friend Testing**
  - [ ] Friends can access app
  - [ ] Friends can sign up
  - [ ] Friends can add vehicles and fuel entries
  - [ ] Each friend's data is separate (data isolation working)

- [ ] **Real Data Testing**
  - [ ] Import your Excel file (MC_Average_23_07_26.xlsx)
  - [ ] Verify 120 records imported correctly
  - [ ] Check calculations match your expectations
  - [ ] Analytics show correct trends

---

## ✅ PHASE 6: MONITORING & MAINTENANCE

- [ ] **Weekly Checks**
  - [ ] App is online and accessible
  - [ ] Can create new account and test
  - [ ] GitHub Actions workflow succeeded in last 7 days

- [ ] **Monitor Supabase**
  - [ ] Check Supabase dashboard occasionally
  - [ ] Verify project is NOT paused
  - [ ] Check database storage usage (free tier: 500 MB limit)

- [ ] **Update Dependencies (Monthly)**
  - [ ] Run: `pip install --upgrade -r requirements.txt`
  - [ ] Test locally
  - [ ] Push to GitHub
  - [ ] Streamlit Cloud auto-redeployes

---

## ❌ COMMON MISTAKES TO AVOID

- ❌ Committing `.env` file to GitHub (SECURITY RISK!)
- ❌ Using wrong Supabase URL in GitHub Actions (app won't start)
- ❌ Forgetting to add secrets to Streamlit Cloud (app crashes)
- ❌ Not enabling GitHub Actions (project pauses after 7 days)
- ❌ Sharing `.env` file with anyone (CREDENTIALS EXPOSED!)
- ❌ Using production database URL in test (test on dev first!)

---

## 🆘 IF SOMETHING BREAKS

### App shows "Missing Supabase credentials"
1. Check Streamlit Cloud secrets are added
2. Verify SUPABASE_URL and SUPABASE_KEY are correct
3. Click "Reboot app" in Streamlit Cloud settings

### "Cannot connect to database"
1. Verify database tables exist in Supabase SQL Editor
2. Check SUPABASE_KEY is correct anon key (not service_role key)
3. Check internet connection

### "Project paused" error
1. Go to Supabase dashboard
2. Click "Resume project"
3. Check GitHub Actions workflow (may not be running)

### Users can see other users' data
1. Run RLS enable commands in Supabase SQL Editor
2. Or temporarily disable RLS if causing issues

---

## 📞 SUPPORT

- **Supabase Status:** https://status.supabase.com
- **Streamlit Community:** https://discuss.streamlit.io
- **GitHub Issues:** https://github.com/streamlit/streamlit/issues

---

## ✨ YOU'RE DONE!

Congratulations! Your app is live and shareable. 🎉

**Next Steps:**
1. Share URL with friends
2. Collect feedback
3. Plan future features
4. Scale as needed

---

**Last Updated:** January 2025
