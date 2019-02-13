import pytest
from app.models import User, Goal
from sqlalchemy.exc import IntegrityError, DataError
from datetime import datetime, timedelta

# Sample goal data
__title = "Coach my Abs"
__description = "Some good things to mention here"
__duedate = datetime.utcnow() + timedelta(days=30)


def create_goal(db, title, user_id, description=None, duedate=None):
    goal = Goal(title=title, user_id=user_id,
                description=description, duedate=duedate)

    db.session.add(goal)
    db.session.commit()
    return goal


def test_goal_creation(dbc, test_user):
    goal = create_goal(dbc, __title, test_user.id, __description, __duedate)

    rv = Goal.query.filter(Goal.title == __title).one()
    assert rv.description == __description
    assert rv.duedate == __duedate
    assert rv.user_id == test_user.id
    assert rv in test_user.goals


def test_goal_creation_no_user(dbc):
    with pytest.raises(TypeError) as e:
        goal = create_goal(db=dbc, title=__title,
                           description=__description, duedate=__duedate)

    assert "user_id" in str(e)


def test_goal_creation_no_title(dbc, test_user):
    with pytest.raises(TypeError) as e:
        goal = create_goal(db=dbc, user_id=test_user.id,
                           description=__description, duedate=__duedate)

    assert "title" in str(e)


def test_goal_creation_no_description(dbc, test_user):
    # goal = create_goal(db=dbc, title=__title, user_id=test_user.id, description=__description, duedate=__duedate)
    goal = create_goal(db=dbc, title=__title,
                       user_id=test_user.id, duedate=__duedate)

    rv = Goal.query.filter(Goal.title == __title).one()
    assert rv.description is None
    assert rv.duedate == __duedate
    assert rv.user_id == test_user.id


def test_goal_creation_no_duedate(dbc, test_user):
    goal = create_goal(db=dbc, title=__title, user_id=test_user.id,
                       description=__description)

    rv = Goal.query.filter(Goal.title == __title).one()
    assert rv.description == __description
    assert rv.duedate is None
    assert rv.user_id == test_user.id


def test_goal_editing(dbc, test_user):
    goal = create_goal(dbc, __title, test_user.id, __description, __duedate)

    rv = Goal.query.filter(Goal.id == goal.id).one()
    rv.title = "Hey, It's a new goal title"

    dbc.session.commit()


def test_goals_of_user(dbc, test_user):
    goal1 = create_goal(dbc, "Goal #1", user_id=test_user.id)
    goal2 = create_goal(dbc, "Goal #2", user_id=test_user.id)
    goal3 = create_goal(dbc, "Goal #3", user_id=test_user.id)

    assert goal1 in test_user.goals
    assert goal2 in test_user.goals
    assert goal3 in test_user.goals


def test_goal_deletion(dbc, test_user):
    goal = create_goal(dbc, __title, test_user.id, __description, __duedate)

    assert Goal.query.filter(Goal.title == __title).count() == 1

    dbc.session.delete(goal)

    assert Goal.query.filter(Goal.title == __title).count() == 0
