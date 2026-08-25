# 🚗 MILEAGE TRACKER - SETUP & DEPLOYMENT GUIDE

## ============================================================================
## QUICK START (Development)
## ============================================================================

### Step 1: Setup Supabase Project (5 minutes)

1. Go to https://supabase.com (sign up if needed)
2. Click "New Project"
3. Choose organization, project name: `mileage-tracker`
4. Set password (save it)
5. Select region: `Asia Pacific (Singapore)` for faster access from India
6. Wait for project to initialize (~1 minute)

### Step 2: Create Database Tables

1. In Supabase dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy-paste entire content of `database_schema.sql`
4. Click "Run"
5. Wait for tables to be created ✓

### Step 3: Get API Keys

1. Go to **Settings → API**
2. Copy the **Project URL** (looks like `https://xxx.supabase.co`)
3. Under API Keys, copy the **anon public key**
4. Paste both into `.env` file (copy from `.env.example`)

### Step 4: Setup Local Development

```bash
# Clone or create project directory
mkdir mileage-tracker
cd mileage-tracker

# Copy files here
# - app.py
# - requirements.txt
# - .env (with your Supabase credentials)

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

✅ App opens at `http://localhost:8501`

Test it:
- Create account
- Add vehicle
- Add fuel entry
- Check dashboard

---

## ============================================================================
## DEPLOYMENT (Make It Publicly Shareable)
## ============================================================================

### Option A: Streamlit Cloud (Recommended - 5 minutes)

**Best for:** Easy deployment, automatic updates, shareable link

1. Push code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/mileage-tracker.git
   git push -u origin main
   ```

2. Go to https://streamlit.io/cloud
3. Sign in with GitHub
4. Click "New app"
5. Repository: `YOUR_USERNAME/mileage-tracker`
6. Branch: `main`
7. Main file path: `app.py`
8. Click "Deploy"

**Configure Secrets:**
1. After deployment, click "..." menu → Settings
2. Go to Secrets
3. Add:
   ```
   SUPABASE_URL = "https://xxx.supabase.co"
   SUPABASE_KEY = "your-anon-key"
   ```
4. Reboot app

✅ Your app is now live at `https://your-username-mileage-tracker.streamlit.app`
✅ Share this URL with anyone!

---

### Option B: Vercel (Alternative - Better performance)

**Best for:** Professional hosting, faster performance, more control

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. Follow prompts (link GitHub account, etc.)

4. Add environment variables:
   ```
   SUPABASE_URL = your-url
   SUPABASE_KEY = your-key
   ```

5. Deploy again:
   ```bash
   vercel --prod
   ```

✅ App is live at `https://your-project.vercel.app`

---

## ============================================================================
## GITHUB ACTIONS SETUP (Keep App Active 24/7)
## ============================================================================

**Why:** Supabase free tier pauses after 7 days of inactivity. This keeps it running.

### Setup Keep-Alive Workflow:

1. In GitHub repository, create folder: `.github/workflows/`
2. Copy `keep-alive.yml` to `.github/workflows/keep-alive.yml`
3. Edit the file:
   - Replace `https://your-project-id.supabase.co` with your actual Supabase URL
4. Commit and push to GitHub

5. In GitHub, go to **Settings → Secrets and variables → Actions**
6. Add secrets:
   - `SUPABASE_URL` = your Supabase URL
   - `SUPABASE_KEY` = your anon key

7. In **Actions** tab, enable workflows if needed
8. Done! The workflow will run every 5 minutes automatically.

✅ Your app now stays online 24/7 without manual intervention.

---

## ============================================================================
## STRUCTURE
## ============================================================================

```
mileage-tracker/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── database_schema.sql       # Supabase database setup
├── .env                      # Your secrets (DON'T COMMIT THIS!)
├── .env.example              # Template for .env
├── .gitignore                # Ignore sensitive files
├── .github/
│   └── workflows/
│       └── keep-alive.yml    # GitHub Actions for 24/7 uptime
└── SETUP_GUIDE.md            # This file
```

---

## ============================================================================
## FEATURES INCLUDED
## ============================================================================

✅ **Authentication**
- Email/password signup & login
- Secure password hashing
- Per-user data isolation

✅ **Multi-Car Support**
- Track multiple vehicles per user
- Switch between cars instantly
- Separate analytics per vehicle

✅ **Core Features**
- Add fuel entries with auto-calculation
- Automatic mileage calculation (KM/L)
- Cost per KM tracking
- Full fuel history with edit/delete

✅ **Analytics**
- Weekly/Monthly/Yearly averages
- 90-day trend charts
- Cost breakdown
- CO2 emissions tracking

✅ **Data Management**
- Import Excel files (bulk upload)
- Export as CSV
- View/Delete individual entries

✅ **UI/UX**
- Clean, mobile-responsive interface
- Real-time calculations
- Plotly interactive charts
- Sidebar navigation

---

## ============================================================================
## DATABASE SCHEMA
## ============================================================================

**users** - User accounts
- id, email, password_hash, created_at

**vehicles** - Cars tracked
- id, user_id, model, registration, created_at

**fuel_records** - Individual fuel entries
- id, vehicle_id, date, fuel_filled, km, cost, mileage (calculated), cost_per_km

**imports** - Track data imports
- id, user_id, file_name, records_imported, created_at

---

## ============================================================================
## TROUBLESHOOTING
## ============================================================================

### "Missing Supabase credentials" error
→ Check `.env` file has SUPABASE_URL and SUPABASE_KEY

### "Supabase connection failed"
→ Verify URL and key are correct (copy from Settings → API)
→ Check internet connection

### "Password incorrect" on login
→ Passwords are hashed. Make sure you're entering correct password.

### Excel import shows errors
→ Check Excel has columns: Date, Mieleage KM, Qty (Ltr), Rate, Total Cost
→ Data must start from row 4 (rows 1-3 are skipped)

### Streamlit Cloud shows "Secrets not found"
→ Add secrets in Streamlit Cloud Settings, then reboot app

### "Project paused" error
→ GitHub Actions didn't run. Check Actions tab, make sure workflow is enabled
→ Manually resume project in Supabase dashboard (temporary fix)

---

## ============================================================================
## SECURITY NOTES
## ============================================================================

⚠️ **DO NOT:**
- Commit `.env` file to GitHub
- Share your Supabase anon key publicly
- Use weak passwords

✅ **DO:**
- Add `.env` to `.gitignore`
- Use strong passwords (8+ chars, mix of symbols)
- Enable Supabase RLS (Row Level Security) for production
- Keep dependencies updated

---

## ============================================================================
## NEXT STEPS
## ============================================================================

1. **Test locally** - Run `streamlit run app.py` and test all features
2. **Deploy to Streamlit Cloud** - Follow Option A above
3. **Share URL** - Give friends the public link
4. **Setup GitHub Actions** - Ensure 24/7 uptime
5. **Monitor** - Check dashboard, watch for errors

---

## ============================================================================
## SUPPORT / ISSUES
## ============================================================================

**Streamlit docs:** https://docs.streamlit.io
**Supabase docs:** https://supabase.com/docs
**GitHub Actions:** https://docs.github.com/en/actions

---

**Built by:** Ojas Paradkar
**Last updated:** January 2025
