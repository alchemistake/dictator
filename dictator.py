import psycopg2
from flask import Flask, request, redirect, flash, url_for, render_template
from flask_login import LoginManager, login_required, logout_user, current_user, UserMixin, login_user
from datetime import datetime

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
    cur.execute("select * from topic where topic_id=%s", (topic_id,))
    topic = cur.fetchone()
    cur.execute("""select * from subtopic where topic_id=%s;""", (topic_id,))
    subtopics = cur.fetchall()
    print subtopics
    return render_template("topic.html", active_topic=topic[1], topics=["asd", "qwe", "zxc"], topic_id=topic[0],
                           subtopics=subtopics)


@app.route('/profile/<profile_id>')
def profile(profile_id):
    return render_template("profile.html", profile_name=profile_id, profile_id=profile_id,
                           topics=["asd", "qwe", "qweqwe"])


@app.route('/subtopic/<topic_id>-<subtopic_name>')
def subtopic(topic_id, subtopic_name):
    cur.execute(
        """select * from definition,post,"user" where definition_id=post_id AND definer_user=user_id AND definition_id in (select post_id from Enter where topic_id=%s and subtopic_name=%s)""",
        (topic_id, subtopic_name))
    defs = cur.fetchall()
    print defs
    return render_template("subtopic.html", topic_id=topic_id, subtopic_name=subtopic_name, defs=defs)


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
    cur.execute("insert into block values (%s,%s);COMMIT;", (current_user.data[0], int(request.form["to_ban"])))
    return redirect(url_for("root"))


@app.route("/add_topic", methods=["POST"])
@login_required
def add_topic():
    cur.execute(
        "insert into topic(topic_name, topic_date, creator_user) values (%s, %s, %s);commit;select currval('topic_topic_id_seq');",
        (request.form["topic"], datetime.now(), current_user.data[0]))
    topic_id = cur.fetchone()

    return redirect(url_for("topic", topic_id=topic_id[0]))


@app.route("/add_subtopic", methods=["POST"])
@login_required
def add_subtopic():
    cur.execute("""insert into subtopic(topic_id, subtopic_name, adder_user) values (%s, %s, %s);commit;""",
                (int(request.form["topic_id"]), request.form["subtopic"], current_user.data[0]))
    return redirect(url_for("topic", topic_id=int(request.form["topic_id"])))


@app.route("/add_def", methods=["POST"])
@login_required
def add_def():
    cur.execute(""" insert into definition(definition_date, definition, definer_user) values (%s, %s, %s);
                    insert into post values (currval('definition_definition_id_seq'), 0, 0);
                    insert into enter(topic_id, subtopic_name, post_id) values (%s, %s, currval('definition_definition_id_seq'));
                    commit;""",
                (datetime.now(), request.form["text"], current_user.data[0], request.form["topic_id"],
                 request.form["subtopic_name"]))
    return ""

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
