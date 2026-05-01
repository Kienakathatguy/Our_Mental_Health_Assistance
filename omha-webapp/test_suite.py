#!/usr/bin/env python
"""
OMHA Application - Automated Testing Suite
Tests all core features and improvements
"""

import sys
import os
from datetime import datetime

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from omha import app, db
from models import User, DiaryEntry, ForumPost, Comment, Article, Video, ChatMessage, EmotionalInsight
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class TestRunner:
    def __init__(self):
        self.app = app
        self.ctx = app.app_context()
        self.ctx.push()
        self.passed = 0
        self.failed = 0

    def log_pass(self, test_name):
        print(f"✓ {test_name}")
        self.passed += 1

    def log_fail(self, test_name, reason):
        print(f"✗ {test_name}: {reason}")
        self.failed += 1

    def test_database_connection(self):
        """Test 1: Database Connection"""
        try:
            User.query.count()
            self.log_pass("Database connection")
        except Exception as e:
            self.log_fail("Database connection", str(e))

    def test_user_creation(self):
        """Test 2: User Creation & Password Hashing"""
        try:
            # Clean up test user if exists
            test_user = User.query.filter_by(username="test_user_001").first()
            if test_user:
                db.session.delete(test_user)
                db.session.commit()

            # Create new user
            user = User(username="test_user_001")
            user.set_password("testpass123")
            db.session.add(user)
            db.session.commit()

            # Verify password hashing
            if user.check_password("testpass123") and not user.check_password("wrongpass"):
                self.log_pass("User creation & password hashing")
            else:
                self.log_fail("User creation & password hashing", "Password verification failed")

            # Cleanup
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            self.log_fail("User creation & password hashing", str(e))

    def test_diary_entry_user_association(self):
        """Test 3: Diary Entry User Association"""
        try:
            user = User(username="test_diary_user")
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()

            entry = DiaryEntry(
                content="Test diary entry",
                emotion="😊",
                user_id=user.id
            )
            db.session.add(entry)
            db.session.commit()

            # Verify association
            retrieved_entry = DiaryEntry.query.filter_by(user_id=user.id).first()
            if retrieved_entry and retrieved_entry.content == "Test diary entry":
                self.log_pass("Diary entry user association")
            else:
                self.log_fail("Diary entry user association", "Entry not found for user")

            # Cleanup
            db.session.delete(entry)
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            self.log_fail("Diary entry user association", str(e))

    def test_forum_post_creation(self):
        """Test 4: Forum Post Creation"""
        try:
            user = User(username="test_forum_user")
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()

            post = ForumPost(
                title="Test Post",
                content="This is a test forum post",
                user_id=user.id
            )
            db.session.add(post)
            db.session.commit()

            # Verify
            retrieved_post = ForumPost.query.filter_by(title="Test Post").first()
            if retrieved_post and retrieved_post.user_id == user.id:
                self.log_pass("Forum post creation")
            else:
                self.log_fail("Forum post creation", "Post not found")

            # Cleanup
            db.session.delete(post)
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            self.log_fail("Forum post creation", str(e))

    def test_comment_creation(self):
        """Test 5: Comment Creation & Sorting"""
        try:
            user = User(username="test_comment_user")
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()

            post = ForumPost(
                title="Comment Test Post",
                content="Test post for comments",
                user_id=user.id
            )
            db.session.add(post)
            db.session.commit()

            # Create multiple comments
            for i in range(3):
                comment = Comment(
                    content=f"Comment {i}",
                    post_id=post.id,
                    user_id=user.id
                )
                db.session.add(comment)
            db.session.commit()

            # Verify sorting (newest first)
            comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.created_at.desc()).all()
            if len(comments) == 3 and comments[0].content == "Comment 2":
                self.log_pass("Comment creation & sorting")
            else:
                self.log_fail("Comment creation & sorting", "Comments not sorted correctly")

            # Cleanup
            for comment in comments:
                db.session.delete(comment)
            db.session.delete(post)
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            self.log_fail("Comment creation & sorting", str(e))

    def test_chat_message_persistence(self):
        """Test 6: Chat Message Persistence"""
        try:
            user = User(username="test_chat_user")
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()

            msg = ChatMessage(
                user_id=user.id,
                role="user",
                content="Hello chatbot"
            )
            db.session.add(msg)
            db.session.commit()

            # Verify retrieval
            retrieved_msg = ChatMessage.query.filter_by(user_id=user.id).first()
            if retrieved_msg and retrieved_msg.content == "Hello chatbot":
                self.log_pass("Chat message persistence")
            else:
                self.log_fail("Chat message persistence", "Message not found")

            # Cleanup
            db.session.delete(msg)
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            self.log_fail("Chat message persistence", str(e))

    def test_emotional_insight_storage(self):
        """Test 7: Emotional Insight Storage"""
        try:
            user = User(username="test_insight_user")
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()

            insight = EmotionalInsight(
                user_id=user.id,
                emotion_type="anxiety",
                description="User feels anxious before exams",
                trigger="before exams",
                frequency="frequent"
            )
            db.session.add(insight)
            db.session.commit()

            # Verify retrieval
            retrieved_insight = EmotionalInsight.query.filter_by(user_id=user.id).first()
            if retrieved_insight and retrieved_insight.emotion_type == "anxiety":
                self.log_pass("Emotional insight storage")
            else:
                self.log_fail("Emotional insight storage", "Insight not found")

            # Cleanup
            db.session.delete(insight)
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            self.log_fail("Emotional insight storage", str(e))

    def test_article_and_video_models(self):
        """Test 8: Article & Video Models"""
        try:
            article = Article(
                title="Mental Health Tips",
                content="Here are some tips...",
                author="Dr. Smith",
                category="Mental Health"
            )
            db.session.add(article)
            db.session.commit()

            video = Video(
                title="Relaxation Techniques",
                description="Learn how to relax",
                video_url="https://youtube.com/watch?v=123"
            )
            db.session.add(video)
            db.session.commit()

            # Verify both exist
            if Article.query.count() > 0 and Video.query.count() > 0:
                self.log_pass("Article & video models")
            else:
                self.log_fail("Article & video models", "Models not saving correctly")

            # Cleanup
            db.session.delete(article)
            db.session.delete(video)
            db.session.commit()
        except Exception as e:
            self.log_fail("Article & video models", str(e))

    def test_route_availability(self):
        """Test 9: Route Availability"""
        try:
            required_routes = [
                '/',
                '/login',
                '/logout',
                '/register',
                '/diary',
                '/forum',
                '/articles',
                '/chatbot',
                '/chatbot/send',
                '/chatbot/clear'
            ]
            
            app_routes = [str(rule) for rule in app.url_map.iter_rules()]
            missing = [r for r in required_routes if r not in app_routes]
            
            if not missing:
                self.log_pass("All required routes available")
            else:
                self.log_fail("Route availability", f"Missing routes: {missing}")
        except Exception as e:
            self.log_fail("Route availability", str(e))

    def test_imports(self):
        """Test 10: Critical Imports"""
        try:
            from services.emotional_analysis import (
                detect_crisis_signals,
                analyze_and_store_insights,
                generate_personalized_prompt_injection,
                get_crisis_response
            )
            self.log_pass("Emotional analysis imports")
        except Exception as e:
            self.log_fail("Emotional analysis imports", str(e))

    def test_error_handling(self):
        """Test 11: Error Handling (Database Rollback)"""
        try:
            # Try to create user with duplicate username
            user1 = User(username="duplicate_test")
            user1.set_password("pass123")
            db.session.add(user1)
            db.session.commit()

            # Try to create another with same username (should fail)
            user2 = User(username="duplicate_test")
            user2.set_password("pass456")
            db.session.add(user2)
            
            try:
                db.session.commit()
                self.log_fail("Error handling", "Should have raised IntegrityError")
            except Exception:
                db.session.rollback()
                self.log_pass("Error handling (rollback)")

            # Cleanup
            db.session.delete(user1)
            db.session.commit()
        except Exception as e:
            self.log_fail("Error handling", str(e))

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*50)
        print("OMHA Application Test Suite")
        print("="*50 + "\n")

        self.test_database_connection()
        self.test_user_creation()
        self.test_diary_entry_user_association()
        self.test_forum_post_creation()
        self.test_comment_creation()
        self.test_chat_message_persistence()
        self.test_emotional_insight_storage()
        self.test_article_and_video_models()
        self.test_route_availability()
        self.test_imports()
        self.test_error_handling()

        print("\n" + "="*50)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("="*50 + "\n")

        return self.failed == 0


if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)
