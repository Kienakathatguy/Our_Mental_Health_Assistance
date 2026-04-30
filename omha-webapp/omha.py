import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit, join_room
from dotenv import load_dotenv

import os

from models import db, User, DiaryEntry, ForumPost, Comment, Article, Video, ChatMessage
from services.chatbot_service import call_chatbot_api

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
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    if request.method == "POST":
        content = request.form["entry"]
        emotion = request.form.get("emotion", "")
        new_entry = DiaryEntry(content=content, emotion=emotion)
        db.session.add(new_entry)
        db.session.commit()
        return redirect("/diary")

    entries = DiaryEntry.query.filter_by(user_id=current_user.id).all()
    return render_template("diary.html", entries=entries)

@app.route("/diary/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_diary(id):
    entry = DiaryEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash("You are not authorised to edit this entry.", "danger")
        return redirect("/diary")
    if request.method == "POST":
        entry.content = request.form["entry"]
        entry.emotion = request.form.get("emotion", entry.emotion)
        db.session.commit()
        return redirect("/diary")
    return render_template("edit_diary.html", entry=entry)

@app.route("/diary/delete/<int:id>")
@login_required
def delete_diary(id):
    entry = DiaryEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash("You are not authorised to delete this entry.", "danger")
        return redirect("/diary")
    db.session.delete(entry)
    db.session.commit()
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

        post = ForumPost(title=form.title.data, content=form.content.data, image=image_path, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('forum'))

    return render_template('create_post.html')

@app.route("/forum/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("You must be logged in to comment.", "danger")
            return redirect(url_for('login'))
        content = request.form.get('content')
        if content:
            new_comment = Comment(content=content, post_id=post_id, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
        return redirect(url_for('view_post', post_id=post_id))

    return render_template('view_post.html', post=post, comments=comments)

@app.route("/articles")
def articles():
    articles = Article.query.order_by(Article.date_posted.desc()).all()
    videos = Video.query.order_by(Video.date_posted.desc()).all()
    
    # Kết hợp bài viết và video lại thành một danh sách (tùy theo nhu cầu, có thể sắp xếp chung)
    all_content = articles + videos

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
        return redirect(url_for("chatbot"))

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

    # 🔥 CALL GEMINI HERE
    reply_text = call_chatbot_api(messages)

    # Save bot reply
    bot_msg = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=reply_text
    )
    db.session.add(bot_msg)
    db.session.commit()

    return redirect(url_for("chatbot"))


@app.route("/chatbot/clear", methods=["POST"])
@login_required
def chatbot_clear():
    ChatMessage.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("Đã xoá lịch sử chat.", "info")
    return redirect(url_for("chatbot"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)