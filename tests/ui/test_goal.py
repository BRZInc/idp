from datetime import datetime, timedelta
from app.models import User, Goal

__title = "Some goal title"
__description = "Test description for the goal"
__duedate = datetime.utcnow()
__private = False
__id = 1

# Goal tests


def test_goals_list(client, log_user):
    rv = client.get('/goals')

    assert rv.status_code == 200
    assert "My Development Goals" in rv.data.decode()


def test_user_without_goals(client, log_user_without_goals):
    rv = client.get('/goals')

    assert rv.status_code == 200
    assert "Add a New Goal" in rv.data.decode()


def test_goal_non_existing(client, log_user):
    # No such goal exists in DB
    rv = client.get('/goals/12323', follow_redirects=True)

    assert rv.status_code == 404


def test_goal_existing(client, log_user):
    g = Goal.query.get(2)
    rv = client.get('/goals/2', follow_redirects=True)

    assert rv.status_code == 200

    d = rv.data.decode()
    assert g.title in d
    assert g.description in d
    assert g.duedate.strftime("%d.%m.%Y") in d


def test_goal_create(client, log_user):
    rv = client.post('/goals/new', data=dict({
        'title': __title,
        'description': __description,
        'duedate': __duedate.strftime("%d.%m.%Y")
    }), follow_redirects=True)

    assert rv.status_code == 200
    assert "Goal has been successfully created!" in rv.data.decode()

    # Reload and try again
    rv = client.get('/goals/4')
    assert rv.status_code == 200


def test_goal_duedate_past(client, log_user):
    past_date = datetime.utcnow() - timedelta(days=30)

    rv = client.post('/goals/new', data=dict({
        'title': __title + "1",
        'description': __description + "1",
        'duedate': past_date.strftime("%d.%m.%Y")
    }), follow_redirects=True)

    assert rv.status_code == 200
    assert 'Please select DueDate &gt;= today' in rv.data.decode()


def test_goal_without_subgoals(client, log_user_without_description):
    rv = client.get('/goals/1', follow_redirects=True)

    assert rv.status_code == 200

    d = rv.data.decode()
    assert "Subgoals" not in d


def test_goal_edit(client, log_user):
    rv = client.post('/goals/2/edit', data=dict({
        'title': __title + "1",
        'description': __description + "1",
        'duedate': (__duedate + timedelta(days=10)).strftime("%d.%m.%Y")
    }), follow_redirects=True)

    assert rv.status_code == 200
    assert "Goal has been updated successfully!" in rv.data.decode()


def test_goal_delete(client, log_user):
    rv = client.get('/goals/3/delete', follow_redirects=True)
    assert rv.status_code == 200
    assert "Goal has been deleted!" in rv.data.decode()
