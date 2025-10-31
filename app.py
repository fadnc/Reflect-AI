from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv

from config import MODEL, COPING_STRATEGIES, CRISIS_RESOURCES, EMOJI_MAP
from database import init_db, insert_entry, load_entries
from ai_engine import generate_reflection
from emotion_analysis import analyze_emotion, get_emotion_category, get_emotion_severity
from utils import (
    crisis_detect, get_similar_entries, get_emotion_patterns, 
    get_sentiment_trends, get_emotion_triggers, get_low_sentiment_context
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Initialize database
init_db()

@app.route('/')
def index():
    """Main dashboard page"""
    df = load_entries()
    
    # Calculate dashboard metrics
    dashboard_data = {
        'total_entries': 0,
        'avg_sentiment': 0,
        'most_common_emotion': 'N/A',
        'positive_count': 0,
        'last_entry': None
    }
    
    if not df.empty:
        df['timestamp'] = df['timestamp'].astype(str)
        dashboard_data = {
            'total_entries': len(df),
            'avg_sentiment': round(df['sentiment'].mean(), 2),
            'most_common_emotion': df['emotion'].mode()[0] if not df['emotion'].mode().empty else 'N/A',
            'positive_count': len(df[df['sentiment'] > 0.3]),
            'last_entry': df.iloc[0].to_dict() if len(df) > 0 else None
        }
    
    emotions = sorted(df['emotion'].unique().tolist()) if not df.empty else []
    
    return render_template('index.html', 
                         dashboard=dashboard_data, 
                         emotions=emotions,
                         emoji_map=EMOJI_MAP)

@app.route('/journal')
def journal():
    """Journal entry page"""
    return render_template('journal.html', emoji_map=EMOJI_MAP)

@app.route('/api/generate-reflection', methods=['POST'])
def api_generate_reflection():
    """API endpoint to generate AI reflection"""
    data = request.json
    entry_text = data.get('entry', '').strip()
    
    if not entry_text:
        return jsonify({'error': 'Entry text is required'}), 400
    
    # Analyze emotion and sentiment
    sentiment, emotion = analyze_emotion(entry_text)
    crisis_level = crisis_detect(entry_text)
    
    # Handle crisis situation
    if crisis_level:
        entry_data = {
            "timestamp": datetime.now().isoformat(),
            "entry": entry_text,
            "reflection": "Crisis support flagged",
            "summary": "Safety resources provided",
            "followups": [],
            "tone": "alert",
            "safety": crisis_level,
            "sentiment": sentiment,
            "emotion": emotion
        }
        insert_entry(entry_data)
        
        return jsonify({
            'crisis': True,
            'crisis_level': crisis_level,
            'resources': CRISIS_RESOURCES,
            'sentiment': sentiment,
            'emotion': emotion
        })
    
    # Generate reflection
    result = generate_reflection(entry_text, emotion, sentiment)
    
    if "error" in result:
        return jsonify({'error': result['error']}), 500
    
    # Save entry to database
    entry_data = {
        "timestamp": datetime.now().isoformat(),
        "entry": entry_text,
        "reflection": result.get("reflection", ""),
        "summary": result.get("summary", ""),
        "followups": result.get("followups", []),
        "tone": result.get("tone", ""),
        "safety": result.get("safety_flag", False),
        "sentiment": sentiment,
        "emotion": emotion
    }
    insert_entry(entry_data)
    
    # Get similar entries
    df = load_entries()
    similar = get_similar_entries(entry_text, df, top_n=3)
    similar_list = similar.to_dict('records') if not similar.empty else []
    
    # Get severity
    severity = get_emotion_severity(sentiment)
    
    return jsonify({
        'reflection': result.get('reflection'),
        'summary': result.get('summary'),
        'actionable_insight': result.get('actionable_insight'),
        'followups': result.get('followups', []),
        'tone': result.get('tone'),
        'coping_suggestion': result.get('coping_suggestion'),
        'sentiment': sentiment,
        'emotion': emotion,
        'severity': severity,
        'similar_entries': similar_list,
        'emoji': EMOJI_MAP.get(emotion.lower(), '')
    })

@app.route('/search')
def search():
    """Search and filter page"""
    df = load_entries()
    emotions = sorted(df['emotion'].unique().tolist()) if not df.empty else []
    return render_template('search.html', emotions=emotions, emoji_map=EMOJI_MAP)

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for searching entries"""
    data = request.json
    search_query = data.get('query', '').lower()
    emotion_filter = data.get('emotions', [])
    sentiment_range = data.get('sentiment_range', [-1.0, 1.0])
    sort_by = data.get('sort_by', 'newest')
    
    df = load_entries()
    
    if df.empty:
        return jsonify({'entries': [], 'count': 0})
    
    # Apply filters
    filtered = df.copy()
    
    if search_query:
        filtered = filtered[filtered['entry'].str.lower().str.contains(search_query, na=False)]
    
    if emotion_filter:
        filtered = filtered[filtered['emotion'].isin(emotion_filter)]
    
    filtered = filtered[
        (filtered['sentiment'] >= sentiment_range[0]) & 
        (filtered['sentiment'] <= sentiment_range[1])
    ]
    
    # Sort
    if sort_by == 'newest':
        filtered = filtered.sort_values('timestamp', ascending=False)
    elif sort_by == 'oldest':
        filtered = filtered.sort_values('timestamp', ascending=True)
    elif sort_by == 'positive':
        filtered = filtered.sort_values('sentiment', ascending=False)
    else:  # negative
        filtered = filtered.sort_values('sentiment', ascending=True)
    
    entries = filtered.to_dict('records')
    
    return jsonify({
        'entries': entries,
        'count': len(entries)
    })

@app.route('/analytics')
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

@app.route('/api/analytics')
def api_analytics():
    """API endpoint for analytics data"""
    df = load_entries()
    
    if df.empty:
        return jsonify({'empty': True})
    
    # Calculate metrics
    total = len(df)
    avg_sentiment = round(df['sentiment'].mean(), 2)
    positive_pct = round((len(df[df['sentiment'] > 0.3]) / total * 100), 0)
    days_span = (df['timestamp'].max() - df['timestamp'].min()).days
    
    # Sentiment over time data
    sentiment_data = df[['timestamp', 'sentiment']].to_dict('records')
    
    # Emotion distribution
    emotion_counts = df['emotion'].value_counts().to_dict()
    
    # Recent entries
    recent = df.head(10).to_dict('records')
    
    return jsonify({
        'empty': False,
        'metrics': {
            'total': total,
            'avg_sentiment': avg_sentiment,
            'positive_pct': positive_pct,
            'days_span': days_span
        },
        'sentiment_data': sentiment_data,
        'emotion_counts': emotion_counts,
        'recent_entries': recent
    })

@app.route('/insights')
def insights():
    """Insights page"""
    return render_template('insights.html', emoji_map=EMOJI_MAP)

@app.route('/api/insights')
def api_insights():
    """API endpoint for insights data"""
    df = load_entries()
    
    if df.empty:
        return jsonify({'empty': True})
    
    patterns = get_emotion_patterns(df)
    transitions = get_emotion_triggers(df)
    low_context = get_low_sentiment_context(df)
    
    return jsonify({
        'empty': False,
        'patterns': patterns,
        'transitions': transitions,
        'low_context': low_context
    })

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
