# 🚀 ReflectAI Flask Deployment Guide

## 📁 Project Structure

After adding files to your repo, you should have:

```
empathy-bot-flask/
├── app.py                    # Main Flask app ✅
├── ai_engine.py              # (Keep existing) ✅
├── emotion_analysis.py       # (Keep existing) ✅
├── database.py               # (Keep existing) ✅
├── config.py                 # Updated version ✅
├── utils.py                  # (Keep existing) ✅
├── requirements.txt          # Updated for Flask ✅
├── .env.example              # Create this ⭐
├── .gitignore                # Create this ⭐
├── README.md                 # Updated guide ✅
├── Procfile                  # For Heroku (optional) ⭐
└── templates/
    ├── base.html            ✅
    ├── index.html           ✅
    ├── journal.html         ✅
    ├── search.html          ✅
    ├── analytics.html       ✅
    ├── insights.html        ✅
    └── about.html           ✅
```

---

## 🔧 Step 1: Setup on GitHub

### Create these NEW files in your repo:

**1. `.env.example`** (template for environment variables):
```bash
# Copy this to .env and fill in your values
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_random_secret_key_here
DB_PATH=journal_entries.db
```

**2. `.gitignore`**:
```
# Environment
.env
venv/
env/
__pycache__/
*.pyc
*.pyo

# Database
*.db
journal_entries.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**3. `Procfile`** (for Heroku deployment):
```
web: gunicorn app:app
```

---

## 💻 Step 2: Running Locally

### On Your Local Machine:

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Create `.env` file:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys:
# - Get GEMINI_API_KEY from: https://aistudio.google.com/app/apikeys
# - Generate FLASK_SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
```

Edit `.env`:
```bash
GEMINI_API_KEY=AIza...your_actual_key
FLASK_SECRET_KEY=8f3a4b2c1d9e0f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2
DB_PATH=journal_entries.db
```

6. **Run the app:**
```bash
python app.py
```

7. **Open browser:**
```
http://localhost:5000
```

---

## 🌐 Step 3: Deploy to Cloud

### Option A: Deploy to Render (Recommended - Free Tier)

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. **Click** "New +" → "Web Service"
4. **Connect** your GitHub repository
5. **Configure:**
   - **Name:** reflectai
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. **Add Environment Variables:**
   - Click "Environment" tab
   - Add: `GEMINI_API_KEY` = your_key
   - Add: `FLASK_SECRET_KEY` = generate_random_key
7. **Click** "Create Web Service"
8. **Wait** for deployment (5-10 minutes)
9. **Access:** `https://reflectai.onrender.com`

---

### Option B: Deploy to Heroku

1. **Install Heroku CLI:**
```bash
# Mac
brew tap heroku/brew && brew install heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login:**
```bash
heroku login
```

3. **Create app:**
```bash
heroku create reflectai-journal
```

4. **Set environment variables:**
```bash
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

5. **Deploy:**
```bash
git push heroku main
```

6. **Open app:**
```bash
heroku open
```

---

### Option C: Deploy to PythonAnywhere (Free Tier)

1. **Sign up:** https://www.pythonanywhere.com
2. **Open** "Web" tab → "Add a new web app"
3. **Choose** "Flask" and Python 3.10
4. **Upload** your code via Files tab
5. **Install** requirements:
```bash
# In PythonAnywhere Bash console:
cd ~
pip install --user -r requirements.txt
```
6. **Set** environment variables in web app config
7. **Reload** web app

---

## 🔑 Generating Secret Keys

**For FLASK_SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output to your `.env` file.

---

## ✅ Verification Checklist

After deployment, test these:

- [ ] Homepage loads with dashboard
- [ ] Can write journal entry
- [ ] AI reflection generates successfully
- [ ] Search and filter works
- [ ] Analytics charts display
- [ ] Insights page shows patterns
- [ ] About page loads

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "Database is locked"

**Solution:**
```bash
# Delete the database and restart
rm journal_entries.db
python app.py
```

### Issue: "API key not valid"

**Solution:**
1. Verify your Gemini API key at https://aistudio.google.com/app/apikeys
2. Check `.env` file has correct key (no spaces, quotes)
3. Restart the Flask app

### Issue: Charts not displaying

**Solution:**
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible
- Try clearing browser cache

---

## 📊 Monitoring & Logs

### View logs locally:
```bash
# Flask shows logs in terminal
python app.py
```

### View logs on Render:
- Dashboard → Your App → "Logs" tab

### View logs on Heroku:
```bash
heroku logs --tail
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** (it's in `.gitignore`)
2. **Use environment variables** for all secrets
3. **Rotate API keys** regularly
4. **Use HTTPS** in production (Render/Heroku do this automatically)
5. **Backup database** regularly

---

## 📈 Scaling Tips

For production use:

1. **Use PostgreSQL** instead of SQLite:
```python
# In database.py, replace SQLite with PostgreSQL
import psycopg2
```

2. **Add Redis** for session management:
```bash
pip install Flask-Session redis
```

3. **Enable CORS** if building separate frontend:
```bash
pip install flask-cors
```

---

## 🆘 Support

If you encounter issues:

1. Check the logs
2. Verify environment variables are set
3. Test API key separately
4. Review GitHub Issues in your repo
5. Check Flask/Render/Heroku documentation

---

## 🎉 You're Done!

Your ReflectAI Flask app should now be running! 🚀

**Next steps:**
- Share the URL with friends
- Start journaling regularly
- Track your emotional patterns
- Provide feedback for improvements
