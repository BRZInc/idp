from app import app
from flask import Flask, render_template, flash, redirect, url_for
from datetime import datetime, timedelta
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
@app.route("/home")
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
			"date": datetime.utcnow()+timedelta(days=1),
			"status": "InProgress"
		}
	]

	return render_template("index.html", title="Rastishka - Home", goals=goals)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)
