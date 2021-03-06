from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, timedelta
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm, GoalForm
from app.models import User, Goal, Subgoal


@app.route("/")
@app.route("/index")
@app.route("/home")
@login_required
def index():
    return render_template("index.html")


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
        user = User(username=form.username.data,
                    first_name=form.firstname.data,
                    last_name=form.lastname.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("You've been successfully registered!")
        return redirect(url_for('login'))

    return render_template("register.html",
                           page_title="Registration",
                           form=form)


@app.route('/user/<username>', methods=["GET"])
@login_required
def user(username):
    user = User.query.filter(User.username == username).first_or_404()

    return render_template("user.html",
                           page_title="Goals of {} {}".format(
                               user.first_name, user.last_name),
                           user=user,
                           goals=user.goals)


@app.route('/goals', methods=['GET'])
@login_required
def goals():
    goals = Goal.query.filter(
        Goal.user_id == current_user.id).order_by(Goal.duedate)

    return render_template("goals.html",
                           page_title="My Development Goals",
                           goals=goals)


@app.route('/goals/<goal_id>', methods=['GET'])
@login_required
def goal_view(goal_id):
    goal = Goal.query.filter(Goal.id == goal_id).first_or_404()

    return render_template("goal.html",
                           page_title="Goal - {}".format(goal.title),
                           goal=goal,
                           user=current_user)


@app.route('/goals/new', methods=['GET', 'POST'])
@login_required
def goal_new():
    form = GoalForm()
    if form.add_subgoal.data:
        form.subgoals.append_entry()
        form.validate = False
    elif any([sg.delete_subgoal.data for sg in form.subgoals.entries]):
        for sg in form.subgoals.entries:
            if sg.delete_subgoal.data:
                form.subgoals.remove(sg)
        form.validate = False
    else:
        if form.validate_on_submit():
            goal = Goal(title=form.title.data,
                        description=form.description.data,
                        duedate=form.duedate.data,
                        user_id=current_user.id)

            for sg in form.subgoals.entries:
                goal.subgoals.append(
                    Subgoal(title=sg.title.data, duedate=sg.duedate.data))

            db.session.add(goal)
            db.session.commit()

            flash("Goal has been successfully created!")
            return redirect(url_for('goal_view', goal_id=goal.id))

    return render_template('goal_new.html',
                           title="Master Lao - Create New Goal",
                           form=form)


@app.route('/goals/<goal_id>/edit', methods=['GET', 'POST'])
@login_required
def goal_edit(goal_id):
    goal = Goal.query.filter(Goal.id == goal_id).first_or_404()

    form = GoalForm()
    if form.add_subgoal.data:
        form.subgoals.append_entry()
        form.validate = False
    elif any([sg.delete_subgoal.data for sg in form.subgoals.entries]):
        for sg in form.subgoals.entries:
            if sg.delete_subgoal.data:
                form.subgoals.remove(sg)
        form.validate = False
    else:
        if request.method == 'POST' and form.validate_on_submit():
            goal.title = form.title.data
            goal.description = form.description.data
            goal.duedate = form.duedate.data

            ids_updated = []
            subgoals_to_save = []
            for sg in form.subgoals.entries:
                if sg.form.id.data:
                    ids_updated.append(int(sg.form.id.data))
                    subgoal = goal.subgoals.filter(
                        Subgoal.id == sg.form.id.data).first()
                    # Don't recreate subgoal if it has
                    # been deleted between form reloads
                    if subgoal:
                        subgoal.title = sg.title.data
                        subgoal.duedate = sg.duedate.data
                else:
                    subgoals_to_save.append(Subgoal(
                        title=sg.title.data,
                        duedate=sg.duedate.data))

            # Remove all subgoals, which have been deleted from the form,
            # but not the new subgoals (those without Id)
            for sg in goal.subgoals:
                if sg.id and sg.id not in ids_updated:
                    db.session.delete(sg)

            goal.subgoals.extend(subgoals_to_save)
            db.session.commit()

            flash("Goal has been updated successfully!")
            return redirect(url_for('goal_view', goal_id=goal.id))
        elif request.method == 'GET':
            form.title.data = goal.title
            form.description.data = goal.description
            form.duedate.data = goal.duedate
            for sg in goal.subgoals:
                form.subgoals.append_entry(sg)

    return render_template("goal_edit.html",
                           goal=goal,
                           form=form,
                           title="Master Lao - Edit Goal")


@app.route('/goals/<goal_id>/delete', methods=['GET'])
@login_required
def goal_delete(goal_id):
    goal = Goal.query.filter(Goal.id == goal_id).first_or_404()

    db.session.delete(goal)
    db.session.commit()

    flash('Goal has been deleted!')
    return redirect(url_for('goals'))
