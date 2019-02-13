from app.models import Subgoal
import pytest
from datetime import datetime, timedelta

__title = "New subgoal title"
__duedate = datetime.utcnow() + timedelta(days=10)


def create_subgoal(db, title, goal_id, duedate=None):
    sg = Subgoal(title=__title, duedate=__duedate, goal_id=goal_id)

    db.session.add(sg)
    db.session.commit()

    return sg


def test_subgoal_creation(dbc, test_user, test_goal):
    sg = create_subgoal(dbc, __title, test_goal.id, __duedate)

    assert sg in test_goal.subgoals
    assert sg.title == __title
    assert sg.duedate == __duedate


def test_subgoal_add_multiple(dbc, test_user, test_goal):
    subgoals = []

    for n in range(0, 3):
        subgoals.append(Subgoal(title="{} #{}".format(
            __title, n), goal_id=test_goal.id))

    dbc.session.add_all(subgoals)
    dbc.session.commit()

    assert Subgoal.query.count() == 3


def test_subgoal_required_values(dbc, test_user, test_goal):
    # No title
    with pytest.raises(TypeError) as e:
        sg = create_subgoal(db=dbc, goal_id=test_goal.id, duedate=__duedate)

    assert "title" in str(e)

    # No goal id
    with pytest.raises(TypeError) as e:
        sg = create_subgoal(db=dbc, title=__title, duedate=__duedate)

    assert "goal_id" in str(e)


def test_subgoal_edit(dbc, test_user, test_goal):
    sg = create_subgoal(dbc, __title, test_goal.id, __duedate)

    sg.title = "Another new title for our subgoal"

    dbc.session.commit()

    res = Subgoal.query.filter(Subgoal.id == sg.id).one()
    assert res.title == "Another new title for our subgoal"


def test_subgoal_deletion(dbc, test_user, test_goal):
    sg = create_subgoal(dbc, __title, test_goal.id, __duedate)

    assert Subgoal.query.filter(Subgoal.title == __title).count() == 1

    dbc.session.delete(sg)
    dbc.session.commit()

    assert Subgoal.query.filter(Subgoal.title == __title).count() == 0
