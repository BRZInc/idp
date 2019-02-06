from app import app, db
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, timedelta
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm
from app.models import User, Goal


@app.route("/")
@app.route("/index")
@app.route("/home")
@login_required
def index():
    goals = [
        {
            "title": "Become best developer in the world",
            "description": "Study: 1. System design 2. Development 3. Practice, practice and practice",
            "date": datetime.utcnow(),
            "status": "Pending"
        },
        {
            "title": "Become best developer in the world",
            "description": "Study: 1. System design 2. Development 3. Practice, practice and practice",
            "date": datetime.utcnow() + timedelta(days=1),
            "status": "InProgress"
        }
    ]

    return render_template("index.html", page_title="Rastishka - Home", goals=goals)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', page_title='Sign In', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.firstname.data,
                    last_name=form.lastname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("You've been successfully registered!")
        return redirect(url_for('login'))

    return render_template("register.html", page_title="Registration", form=form)


@app.route('/user/<username>', methods=["GET"])
@login_required
def user(username):
    user = User.query.filter(User.username == username).first_or_404()

    goals = [
        {
            "title": "Become best developer in the world",
            "description": "Study: 1. System design 2. Development 3. Practice, practice and practice",
            "date": datetime.utcnow(),
            "status": "Pending"
        },
        {
            "title": "Become best developer in the world",
            "description": "Study: 1. System design 2. Development 3. Practice, practice and practice",
            "date": datetime.utcnow() + timedelta(days=1),
            "status": "InProgress"
        }
    ]

    return render_template("user.html", page_title="Goals of {} {}".format(user.first_name, user.last_name), user=user, goals=goals)


@app.route('/goals', methods=['GET'])
@login_required
def goals():
    goals = Goal.query.filter(
        Goal.user_id == current_user.id).order_by(Goal.created_at)
    #goals = Goal.query.order_by(Goal.created_at)

    return render_template("goals.html", page_title="My Development Goals", goals=goals), 200
