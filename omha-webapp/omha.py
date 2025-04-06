from flask import Flask, render_template, request, redirect
from models import db, DiaryEntry, ForumPost

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///omha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/diary", methods=["GET", "POST"])
def diary():
    if request.method == "POST":
        content = request.form["entry"]
        new_entry = DiaryEntry(content=content)
        db.session.add(new_entry)
        db.session.commit()
        return redirect("/diary")
    entries = DiaryEntry.query.order_by(DiaryEntry.id.desc()).all()
    return render_template("diary.html", entries=entries)

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
