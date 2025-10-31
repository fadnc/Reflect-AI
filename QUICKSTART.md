# 🚀 Quick Start Guide - ReflectAI Flask

## 📋 What You Need to Add to Your GitHub Repo

### ✅ Files to REPLACE (update existing files):
1. `app.py` - New Flask version
2. `config.py` - Updated with EMOJI_MAP
3. `requirements.txt` - Flask dependencies

### ✅ Files to ADD (new files):
1. Create `templates/` folder with:
   - `base.html`
   - `index.html`
   - `journal.html`
   - `search.html`
   - `analytics.html`
   - `insights.html`
   - `about.html`
2. `.gitignore`
3. `.env.example`
4. `Procfile`

### ✅ Files to KEEP (don't change):
- `ai_engine.py`
- `emotion_analysis.py`
- `database.py`
- `utils.py`

---

## 🎯 Complete File Structure

```
your-repo/
├── app.py                    ⭐ REPLACE
├── config.py                 ⭐ REPLACE
├── requirements.txt          ⭐ REPLACE
├── ai_engine.py              ✅ KEEP AS IS
├── emotion_analysis.py       ✅ KEEP AS IS
├── database.py               ✅ KEEP AS IS
├── utils.py                  ✅ KEEP AS IS
├── .gitignore                ⭐ NEW FILE
├── .env.example              ⭐ NEW FILE
├── Procfile                  ⭐ NEW FILE
├── README.md                 ⭐ REPLACE (optional)
└── templates/                ⭐ NEW FOLDER
    ├── base.html
    ├── index.html
    ├── journal.html
    ├── search.html
    ├── analytics.html
    ├── insights.html
    └── about.html
```

---

## 💻 How to Run After Adding to GitHub

### Option 1: Clone and Run Locally

```bash
# 1. Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env

# 6. Edit .env and add your Gemini API key
# Get key from: https://aistudio.google.com/app/apikeys
nano .env  # or use any text editor

# Add this to .env:
GEMINI_API_KEY=your_actual_key_here
FLASK_SECRET_KEY=generate_with_command_below
DB_PATH=journal_entries.db

# Generate secret key:
python -c "import secrets; print(secrets.token_hex(32))"

# 7. Run the app
python app.py

# 8. Open browser
# Go to: http://localhost:5000
```

---

### Option 2: Deploy Directly from GitHub (Render)

**🌟 Easiest way - No local setup needed!**

1. **Go to Render.com:**
   - Visit: https://render.com
   - Sign up with your GitHub account

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Select your repository
   - Click "Connect"

3. **Configure:**
   ```
   Name: reflectai
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Add Environment Variables:**
   - Click "Environment" tab
   - Add variables:
     ```
     GEMINI_API_KEY = your_key_from_google
     FLASK_SECRET_KEY = any_random_32_char_string
     ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 5-10 minutes
   - Your app will be live at: `https://reflectai.onrender.com`

---

### Option 3: Deploy to Heroku from GitHub

```bash
# 1. Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew tap heroku/brew && brew install heroku

# 2. Login
heroku login

# 3. Create app (from your local repo)
heroku create your-app-name

# 4. Set environment variables
heroku config:set GEMINI_API_KEY=your_key
heroku config:set FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 5. Deploy
git push heroku main

# 6. Open app
heroku open
```

---

## 🔑 Getting Your Gemini API Key

1. Go to: https://aistudio.google.com/app/apikeys
2. Click "Get API Key" or "Create API Key"
3. Choose "Create API key in new project"
4. Copy the key (starts with `AIza...`)
5. Paste it in your `.env` file or hosting platform

**⚠️ NEVER commit the API key to GitHub!**

---

## 📁 Adding Files to GitHub

### Method 1: Using GitHub Web Interface

1. Go to your repo on GitHub
2. Click "Add file" → "Create new file"
3. Name the file (e.g., `templates/base.html`)
4. Paste the content
5. Commit the file
6. Repeat for all files

### Method 2: Using Git Command Line

```bash
# 1. Clone your repo (if not already)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# 2. Create templates folder
mkdir templates

# 3. Add all the new files (copy them to the folder)

# 4. Stage all changes
git add .

# 5. Commit
git commit -m "Convert Streamlit to Flask"

# 6. Push to GitHub
git push origin main
```

---

## ✅ Testing Checklist

After deployment, verify:

- [ ] Homepage loads (should see dashboard)
- [ ] Can navigate to Journal page
- [ ] Can write and submit journal entry
- [ ] AI reflection generates (may take 10-20 seconds first time)
- [ ] Search page works
- [ ] Analytics charts display
- [ ] Insights page shows data
- [ ] About page loads

---

## 🐛 Common Issues & Solutions

### Issue: "ModuleNotFoundError"
**Solution:** 
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "API key not valid"
**Solution:**
1. Check your API key at https://aistudio.google.com/app/apikeys
2. Verify `.env` has correct key (no quotes, no spaces)
3. Restart the app

### Issue: Database errors
**Solution:**
```bash
# Delete old database and restart
rm journal_entries.db
python app.py
```

### Issue: Port already in use
**Solution:**
```bash
# Change port in app.py (last line):
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Charts not showing
**Solution:**
- Clear browser cache
- Check browser console (F12) for errors
- Ensure internet connection (Chart.js loads from CDN)

---

## 🎓 Learning Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Render Docs:** https://render.com/docs
- **Heroku Docs:** https://devcenter.heroku.com/
- **Bootstrap Docs:** https://getbootstrap.com/docs/

---

## 📞 Need Help?

1. Check the `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Review error messages in terminal/logs
3. Verify all environment variables are set
4. Test Gemini API key separately
5. Check GitHub Issues in your repo

---

## 🎉 Success!

Once everything works:
1. ✅ Your app is live
2. ✅ You can journal from anywhere
3. ✅ Data persists in the database
4. ✅ AI reflections work smoothly

**Enjoy your AI journaling companion! 🧠💜**
