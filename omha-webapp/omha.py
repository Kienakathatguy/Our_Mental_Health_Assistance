from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from models import db, User, DiaryEntry, ForumPost, Comment, Article, Video
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit, join_room
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)
bcrypt = Bcrypt()
migrate = Migrate(app, db)
socketio = SocketIO(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect if user is not logged in

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
def edit_diary(id):
    entry = DiaryEntry.query.get_or_404(id)
    if request.method == "POST":
        entry.content = request.form["entry"]
        entry.emotion = request.form.get("emotion", entry.emotion)
        db.session.commit()
        return redirect("/diary")
    return render_template("edit_diary.html", entry=entry)

@app.route("/diary/delete/<int:id>")
def delete_diary(id):
    entry = DiaryEntry.query.get_or_404(id)
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

@app.route("/forum/<int:post_id>")
def view_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()

    # Nếu là yêu cầu POST (thêm bình luận mới)
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_comment = Comment(content=content, post_id=post_id, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('view_post', post_id=post_id))  # Redirect lại để tránh lỗi double submit

    # Nếu là yêu cầu GET (hiển thị bài viết và bình luận)
    return render_template('view_post.html', post=post, comments=comments)


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        # Nhận tin nhắn từ người dùng
        message_content = request.form["message"]
        new_message = Message(sender=current_user.username, content=message_content)
        db.session.add(new_message)
        db.session.commit()

    # Lấy tất cả tin nhắn từ cơ sở dữ liệu
    messages = Message.query.all()
    return render_template("chat.html", messages=messages)

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
    return render_template("room.html")

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("join", data, room=room)

@socketio.on("signal")
def handle_signal(data):
    room = data["room"]
    emit("signal", data, room=room)

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    reply = ""
    if request.method == "POST":
        msg = request.form["message"]
        if "buồn" in msg:
            reply = "Mình ở đây, bạn không cô đơn đâu 🌱"
        elif "vui" in msg:
            reply = "Thật tuyệt! Hãy chia sẻ niềm vui của bạn nhé!"
        else:
            reply = "Cảm ơn bạn đã chia sẻ. Bạn muốn nói thêm điều gì không?"
    return render_template("chatbot.html", reply=reply)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
