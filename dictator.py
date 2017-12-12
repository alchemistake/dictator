#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, flash, url_for, render_template
from flask_login import LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def root():
    return render_template("index.html", active_topic=None, topics=["asd", "qwe", "zxc"])


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print request.form["email"], request.form["pass"]
    return render_template("login.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print request.form["userName"], request.form["inputEmail"], request.form["inputEmailR"], request.form[
            "inputPassword"], request.form["inputPasswordR"]
    return render_template("signup.html")


@app.route('/topic/<topic_id>')
def topic(topic_id):
    pass


@app.route('/profile/<profile_id>')
def profile(profile_id):
    pass


@app.route('/messages')
@login_required
def messages():
    pass


@app.route('/following')
@login_required
def following():
    pass


@app.route('/logout')
@login_required
def logout_user():
    logout_user()
    return redirect(url_for("root"))


if __name__ == '__main__':
    app.debug = True
    app.run()  # Local Host
    # app.run(host='0.0.0.0')  # Local IP
