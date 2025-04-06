from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, DiaryEntry, ForumPost

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect if user is not logged in

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
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
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


@app.route("/forum", methods=["GET", "POST"])
def forum():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = ForumPost(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect("/forum")
    posts = ForumPost.query.order_by(ForumPost.id.desc()).all()
    return render_template("forum.html", posts=posts)

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/articles")
def articles():
    return render_template("articles.html")

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
