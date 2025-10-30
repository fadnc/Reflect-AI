# 🧠 ReflectAI — Flask Version

AI-Powered Reflective Journaling Companion built with Flask

## 🚀 Quick Start

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_random_secret_key_here
DB_PATH=journal_entries.db
```

Get your Gemini API key from: https://aistudio.google.com/app/apikeys

### 3. Run the Application

```bash
python app.py
```

Visit: http://localhost:5000

## 📁 Project Structure

```
empathy-bot-flask/
├── app.py                  # Main Flask application
├── ai_engine.py            # AI reflection generation
├── emotion_analysis.py     # Emotion & sentiment detection
├── database.py             # SQLite operations
├── config.py               # Configuration
├── utils.py                # Utility functions
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (create this)
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Dashboard
    ├── journal.html       # Journal entry page
    ├── search.html        # Search & filter
    ├── analytics.html     # Analytics dashboard
    ├── insights.html      # Emotional insights
    └── about.html         # About page
```

## 🎯 Features

- **Journal Entries** - Write and reflect with AI-powered insights
- **Emotion Analysis** - 15+ emotions detected automatically
- **Search & Filter** - Find entries by emotion, sentiment, or keywords
- **Analytics Dashboard** - Visualize emotional trends over time
- **Pattern Recognition** - Discover emotional patterns and triggers
- **Crisis Detection** - Automatic flagging with support resources

## 🔧 API Endpoints

- `POST /api/generate-reflection` - Generate AI reflection for journal entry
- `POST /api/search` - Search and filter journal entries
- `GET /api/analytics` - Get analytics data
- `GET /api/insights` - Get emotional insights and patterns

## 🌐 Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t reflectai .
docker run -p 5000:5000 --env-file .env reflectai
```

## ⚠️ Important Notes

- This is NOT a replacement for professional therapy
- If you're in crisis, contact mental health professionals immediately
- Your data is stored locally in SQLite database
- API keys are never logged or exposed

## 📝 License

MIT License - See LICENSE file

## 👨‍💻 Author

Fadhil Muhammed N C - MSc Computer Science (Data Analytics)
