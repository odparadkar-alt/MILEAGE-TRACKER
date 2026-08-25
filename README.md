# 🚗 Mileage Tracker

A web app to track your vehicle's fuel efficiency, costs, and analytics. Works with multiple cars, supports bulk import, and provides real-time mileage calculations.

**Live Demo:** [Coming Soon]

---

## ✨ Features

### Core
- 👤 **User Accounts** - Email/password authentication
- 🚗 **Multi-Car Support** - Track 2+ vehicles per account
- ⛽ **Fuel Entry** - Quick form to add fuel records
- 📊 **Auto-Calculations** - Mileage (KM/L) and cost per KM

### Analytics
- 📈 **Trend Charts** - Visualize mileage over time
- 📋 **Weekly/Monthly/Yearly Stats** - Detailed breakdowns
- 💰 **Cost Analysis** - Total spent, average cost per KM
- 🌍 **CO2 Emissions** - Track environmental impact

### Data Management
- 📥 **Excel Import** - Bulk upload historical data
- 📥 **CSV Export** - Download all records
- ✏️ **Edit/Delete** - Modify entries anytime

### Deployment
- 🌐 **Streamlit Cloud** - Free, shareable public link
- 🔐 **Supabase** - Secure PostgreSQL backend
- ⚡ **GitHub Actions** - Automatic 24/7 keep-alive

---

## 🛠 Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** Supabase (PostgreSQL)
- **Charts:** Plotly
- **Deployment:** Streamlit Cloud
- **Keep-Alive:** GitHub Actions

---

## 🚀 Quick Start

### 1. Setup Supabase (5 min)

```bash
# Go to https://supabase.com
# New Project → Create → Set password
# Copy URL and anon key
```

### 2. Setup Locally

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/mileage-tracker.git
cd mileage-tracker

# Create .env
cp .env.example .env
# Edit .env with your Supabase credentials

# Install & Run
pip install -r requirements.txt
streamlit run app.py
```

✅ Open http://localhost:8501

### 3. Create Database

1. Go to Supabase SQL Editor
2. Copy-paste `database_schema.sql`
3. Run query

### 4. Deploy (Streamlit Cloud)

1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Select repository & branch
4. Add secrets (SUPABASE_URL, SUPABASE_KEY)

✅ App live at `https://username-mileage-tracker.streamlit.app`

### 5. Setup Keep-Alive

Add GitHub Actions secrets:
- `SUPABASE_URL`
- `SUPABASE_KEY`

Workflow runs every 5 minutes → App stays online 24/7

---

## 📱 Screenshots

### Dashboard
- Quick stats (last mileage, monthly cost, trend)
- 30-day trend chart
- Recent entries table

### Add Entry
- Date picker
- Fuel (L), Odometer, Cost inputs
- Auto-calculates mileage

### Analytics
- Weekly/Monthly/Yearly stats
- 90-day trend chart
- CO2 emissions

### Multi-Car
- Switch vehicles instantly
- Separate data per car
- Add new cars anytime

---

## 📋 Project Structure

```
mileage-tracker/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── database_schema.sql       # Supabase schema
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── .streamlit/
│   └── config.toml          # Streamlit config
├── .github/workflows/
│   └── keep-alive.yml       # GitHub Actions workflow
├── SETUP_GUIDE.md           # Detailed setup instructions
└── README.md                # This file
```

---

## 🔐 Security

- Passwords hashed with SHA256
- Environment variables for secrets
- Row-Level Security (RLS) on database
- User data isolation

---

## 📊 Database Schema

**users** - User accounts with credentials
**vehicles** - Multiple cars per user
**fuel_records** - Individual fuel entries with auto-calculated metrics
**imports** - Track bulk imports

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing credentials" | Add SUPABASE_URL and SUPABASE_KEY to .env |
| Login fails | Check .env has correct Supabase keys |
| Excel import errors | Ensure columns match: Date, Mieleage KM, Qty (Ltr), Rate, Total Cost |
| "Project paused" | GitHub Actions may not be running. Check Actions tab. |
| No data appears | Verify database tables created via SQL Editor |

---

## 🚀 Future Enhancements

- [ ] Real-time collaborative tracking
- [ ] Mobile app (React Native)
- [ ] Maintenance alerts & cost prediction
- [ ] Friend comparison & leaderboard
- [ ] Integration with Google Maps
- [ ] SMS/email notifications

---

## 📝 Usage Example

1. **Sign up** → Email & password
2. **Add car** → Model & registration
3. **Add fuel entry** → Date, fuel (L), KM, cost
4. **View dashboard** → See mileage & trends
5. **Import Excel** → Historical data (120 records)
6. **Export CSV** → Download your data

---

## 📞 Support

- **Streamlit Docs:** https://docs.streamlit.io
- **Supabase Docs:** https://supabase.com/docs
- **GitHub Actions:** https://docs.github.com/actions

---

## 📄 License

MIT License - Feel free to use and modify

---

## 👤 Author

Built by **Ojas Paradkar**
- Agency: Nexa Digital
- PGDM E-Business @ WeSchool Mumbai
- Business Analytics Specialization

---

## ⭐ Support

If you find this useful, please star ⭐ the repository!

---

**Last Updated:** January 2025
