#!/bin/bash

# OMHA Application Startup Script

echo "================================"
echo "OMHA Mental Health Companion App"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Please create .env with:"
    echo "  GEMINI_API_KEY=your_key_here"
    echo "  SECRET_KEY=your_secret_key"
    exit 1
fi

echo "✓ .env file found"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python -c "
from omha import app, db
with app.app_context():
    db.create_all()
    print('✓ Database initialized')
"

# Check required tables
echo "📋 Verifying database schema..."
python -c "
from omha import app, db
from models import User, DiaryEntry, ForumPost, Comment, Article, Video, ChatMessage, EmotionalInsight
with app.app_context():
    tables = [User, DiaryEntry, ForumPost, Comment, Article, Video, ChatMessage, EmotionalInsight]
    for table in tables:
        count = table.query.count()
        print(f'  ✓ {table.__name__}: {count} records')
"

echo ""
echo "================================"
echo "✓ Setup complete!"
echo "================================"
echo ""
echo "Starting server..."
echo "🌐 Access app at: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop"
echo ""

# Start the app
python omha.py
