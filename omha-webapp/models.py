from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    entries = db.relationship('DiaryEntry', backref='author', lazy=True)
    emotional_insights = db.relationship('EmotionalInsight', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text, nullable=False)
    emotion = db.Column(db.String(20))  # 👈 Thêm cảm xúc
    theme = db.Column(db.String(50), default='default')
    font = db.Column(db.String(50), default='default')
    background = db.Column(db.String(50), default='default')
    image = db.Column(db.String(200))  # Path to uploaded image
    stickers = db.Column(db.Text)  # JSON string of selected stickers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Thêm khóa ngoại liên kết với bảng User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<DiaryEntry {self.id}>"

class ForumPost(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    image = db.Column(String(200))  # Thêm trường image
    created_at = Column(db.DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship('User', backref='forum_posts', lazy=True)

    def __repr__(self):
        return f"<ForumPost {self.title}>"

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    post = relationship('ForumPost', backref='comments', lazy=True)
    user = relationship('User', backref='comments', lazy=True)

    def __repr__(self):
        return f"<Comment {self.id}>"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50))

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(200), nullable=False)  # URL của video, ví dụ: YouTube URL
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ChatMessage(db.Model):
    """Stores one turn of a chatbot conversation for a user.

    role is either 'user' or 'assistant', mirroring the HF /v1/chat/completions
    message format so the full history can be forwarded directly to the API.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)   # 'user' | 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EmotionalInsight(db.Model):
    """Stores emotional patterns and insights detected from user messages.
    
    This enables the chatbot to remember and reference user patterns over time,
    making responses more personalized and contextual.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Emotional signal type: 'stress', 'anxiety', 'sadness', 'burnout', 'overwhelm', etc.
    emotion_type = db.Column(db.String(50), nullable=False)
    
    # Description of the insight/pattern
    description = db.Column(db.Text, nullable=False)
    
    # Context or trigger (e.g., "before exams", "during group projects")
    trigger = db.Column(db.String(200))
    
    # Frequency: how often this pattern occurs
    frequency = db.Column(db.String(50), default='occasional')  # rare, occasional, frequent
    
    # Last observed date
    last_observed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # When this insight was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<EmotionalInsight {self.emotion_type} for user {self.user_id}>"

    def __repr__(self):
        return f"<ChatMessage {self.role} user={self.user_id}>"