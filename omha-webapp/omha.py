import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit, join_room
from werkzeug.utils import secure_filename, send_from_directory
from dotenv import load_dotenv

import os

from models import db, User, DiaryEntry, ForumPost, Comment, Article, Video, ChatMessage, EmotionalInsight, PostForm
from services.chatbot_service import call_chatbot_api
from services.emotional_analysis import (
    get_journal_prompt,
    get_reflection_prompt,
    get_journal_templates,
    EMOTION_PROMPTS,
)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

UPLOAD_FOLDER = 'uploads/'  # Thư mục chứa hình ảnh
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username đã tồn tại!", "danger")
            return redirect(url_for("register"))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Đăng ký thành công!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Kiểm tra xem người dùng có tồn tại không
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            # Nếu tài khoản không tồn tại hoặc mật khẩu sai, hiển thị lỗi
            flash('Tài khoản hoặc mật khẩu không đúng!', 'danger')
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Đã đăng xuất thành công!", "info")
    return redirect(url_for("login"))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("entry", "").strip()
        emotion = request.form.get("emotion", "")
        theme = request.form.get("theme", "default")
        font = request.form.get("font", "default")
        background = request.form.get("background", "default")
        stickers = request.form.get("stickers", "")
        mode = request.form.get("mode", "full")

        # Handle image upload
        image_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename

        if not content:
            flash("Vui lòng nhập nội dung nhật ký!", "warning")
            return redirect("/diary")
        try:
            new_entry = DiaryEntry(
                title=title,
                content=content,
                emotion=emotion,
                theme=theme,
                font=font,
                background=background,
                image=image_path,
                stickers=stickers,
                user_id=current_user.id,
            )
            db.session.add(new_entry)
            db.session.commit()
            if mode == "quick":
                flash("Lưu nhật ký nhanh thành công!", "success")
            else:
                flash("Lưu nhật ký thành công!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi lưu nhật ký: {str(e)}", "danger")
        return redirect("/diary")

    entries = DiaryEntry.query.filter_by(user_id=current_user.id).order_by(DiaryEntry.created_at.desc()).all()
    prompt = get_journal_prompt()
    reflection_prompt = get_reflection_prompt()
    templates = get_journal_templates()
    return render_template(
        "diary.html",
        entries=entries,
        journal_prompt=prompt,
        reflection_prompt=reflection_prompt,
        journal_templates=templates,
        emotion_prompts=EMOTION_PROMPTS,
    )

@app.route("/diary/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_diary(id):
    entry = DiaryEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash("You are not authorised to edit this entry.", "danger")
        return redirect("/diary")
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("entry", "").strip()
        theme = request.form.get("theme", entry.theme)
        font = request.form.get("font", entry.font)
        background = request.form.get("background", entry.background)
        stickers = request.form.get("stickers", entry.stickers)

        # Handle image upload
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                entry.image = filename

        if not content:
            flash("Vui lòng nhập nội dung!", "warning")
            return redirect(f"/diary/edit/{id}")
        try:
            entry.title = title
            entry.content = content
            entry.emotion = request.form.get("emotion", entry.emotion)
            entry.theme = theme
            entry.font = font
            entry.background = background
            entry.stickers = stickers
            db.session.commit()
            flash("Cập nhật nhật ký thành công!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi cập nhật: {str(e)}", "danger")
        return redirect("/diary")
    return render_template("edit_diary.html", entry=entry)

@app.route("/diary/delete/<int:id>")
@login_required
def delete_diary(id):
    entry = DiaryEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash("You are not authorised to delete this entry.", "danger")
        return redirect("/diary")
    try:
        db.session.delete(entry)
        db.session.commit()
        flash("Đã xóa nhật ký thành công!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Lỗi khi xóa: {str(e)}", "danger")
    return redirect("/diary")


@app.route('/forum')
def forum():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('forum.html', posts=posts)

@app.route('/forum/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        image = form.image.data
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            image_path = None

        post = ForumPost(title=form.title.data, content=form.content.data, image=filename if image else None, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('forum'))

    return render_template('create_post.html', form=form)

@app.route("/forum/<int:post_id>", methods=["GET", "POST"])
@login_required
def view_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("You must be logged in to comment.", "danger")
            return redirect(url_for('login'))
        content = request.form.get('content', '').strip()
        if content:
            try:
                new_comment = Comment(content=content, post_id=post_id, user_id=current_user.id)
                db.session.add(new_comment)
                db.session.commit()
                flash("Bình luận đã được đăng!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Lỗi khi đăng bình luận: {str(e)}", "danger")
        else:
            flash("Vui lòng nhập nội dung bình luận!", "warning")
        return redirect(url_for('view_post', post_id=post_id))

    return render_template('view_post.html', post=post, comments=comments)

@app.route("/articles")
def articles():
    articles = Article.query.order_by(Article.date_posted.desc()).all()
    videos = Video.query.order_by(Video.date_posted.desc()).all()
    
    # Kết hợp bài viết và video lại thành một danh sách và sắp xếp theo ngày
    all_content = sorted(articles + videos, key=lambda x: x.date_posted, reverse=True)

    return render_template("articles.html", all_content=all_content)

@app.route("/article/<int:article_id>")
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("view_article.html", article=article)

@app.route("/video")
def video():
    return render_template("video_call.html")

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("join", data, room=room)

@socketio.on("signal")
def handle_signal(data):
    room = data["room"]
    emit("signal", data, room=room)

MAX_HISTORY = 10

@app.route("/chatbot")
@login_required
def chatbot():
    messages = (
        ChatMessage.query
        .filter_by(user_id=current_user.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return render_template("chatbot.html", messages=messages)


@app.route("/chatbot/send", methods=["POST"])
@login_required
def chatbot_send():
    user_text = request.form.get("message", "").strip()

    if not user_text:
        flash("Vui lòng nhập tin nhắn!", "warning")
        return redirect(url_for("chatbot"))

    try:
        # Save user message
        user_msg = ChatMessage(
            user_id=current_user.id,
            role="user",
            content=user_text
        )
        db.session.add(user_msg)
        db.session.flush()

        # Get recent history
        past_messages = (
            ChatMessage.query
            .filter_by(user_id=current_user.id)
            .order_by(ChatMessage.created_at.desc())
            .limit(MAX_HISTORY * 2)
            .all()
        )
        past_messages.reverse()

        messages = [
            {"role": m.role, "content": m.content}
            for m in past_messages
        ]

        # 🔥 CALL GEMINI API
        reply_text = call_chatbot_api(messages, current_user.id)

        # Save bot reply
        bot_msg = ChatMessage(
            user_id=current_user.id,
            role="assistant",
            content=reply_text
        )
        db.session.add(bot_msg)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Lỗi khi gắp guớe: {str(e)}", "danger")

    return redirect(url_for("chatbot"))


@app.route("/chatbot/save_to_diary/<int:message_id>", methods=["POST"])
@login_required
def save_chat_to_diary(message_id):
    message = ChatMessage.query.get_or_404(message_id)
    if message.user_id != current_user.id:
        flash("You are not authorized to save this message.", "danger")
        return redirect(url_for("chatbot"))
    
    try:
        # Create diary entry from chat message
        diary_entry = DiaryEntry(
            content=f"Chatbot message: {message.content}",
            emotion="🤖",  # Bot emoji
            user_id=current_user.id
        )
        db.session.add(diary_entry)
        db.session.commit()
        flash("Đã lưu tin nhắn vào nhật ký!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Lỗi khi lưu: {str(e)}", "danger")
    return redirect(url_for("chatbot"))


@app.route("/chatbot/clear", methods=["POST"])
@login_required
def chatbot_clear():
    try:
        ChatMessage.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash("Đã xóa lịch sử chảt." , "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Lỗi khi xóa: {str(e)}", "danger")
    return redirect(url_for("chatbot"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✓ Database initialized")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)