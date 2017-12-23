import psycopg2
from flask import Flask, request, redirect, flash, url_for, render_template
from flask_login import LoginManager, login_required, logout_user, current_user, UserMixin, login_user

conn = psycopg2.connect("dbname='postgres' user='Alchemistake'  password='C4NB3GVMA'")
cur = conn.cursor()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, email, data):
        self.email = email
        self.data = data

    def get_id(self):
        return unicode(self.email)

    @classmethod
    def get(cls, email):
        cur.execute("SELECT * FROM \"user\" WHERE user_email=%s;", (email,))
        user = cur.fetchone()
        if user is None:
            return None
        return User(email, user)


@login_manager.user_loader
def load_user(email):
    return User.get(email)


@app.route('/')
def root():
    return render_template("index.html", active_topic=None, topics=["asd", "qwe", "zxc"])


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.get(request.form["email"])
        if user is not None:
            login_user(user)
            return redirect(url_for("root"))
    return render_template("login.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if request.form["inputEmail"] == request.form["inputEmailR"] and request.form["inputPasswordR"] == request.form[
            "inputPassword"]:
            cur.execute(
                'INSERT INTO "user"(user_nickname,user_email,user_password,user_role) VALUES (%s, %s, %s, 1);COMMIT;',
                (request.form["userName"], request.form["inputEmail"], request.form["inputPassword"]))
            return redirect(url_for("root"))
    return render_template("signup.html")


@app.route('/topic/<topic_id>')
def topic(topic_id):
    return render_template("topic.html", active_topic=topic_id, topics=["asd", "qwe", "zxc"], topic_id=topic_id,
                           subtopics=[])


@app.route('/profile/<profile_id>')
def profile(profile_id):
    return render_template("profile.html", profile_name=profile_id, profile_id=profile_id,
                           topics=["asd", "qwe", "qweqwe"])


#
#
# @app.route('/messages')
# @login_required
# def messages():
#     pass
#
#
# @app.route('/following')
# @login_required
# def following():
#     pass
#
@app.route('/ban', methods=["POST"])
@login_required
def ban():
    cur.execute("insert into block values (%s,%s)", (current_user.data[0], int(request.form["to_ban"])))
    return redirect(url_for("root"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("root"))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "dictatordictator"
    app.run()  # Local Host
    # app.run(host='0.0.0.0')  # Local IP
