from datetime import datetime, timedelta

__title = "Some goal title"
__description = "Test description for the goal"
__duedate = datetime.utcnow()
__private = False
__id = 1


def test_goals_list(client):
    rv = client.get('/goals/')
    assert rv.status == "200 OK"
    assert "My goals" in rv.data.decode()

def test_goal_create(client):
    rv = client.post('/goals/new', data=dict({
        'title': __title,
        'description': __description,
        'due_date': __duedate
    }))

    assert rv.status == "201 CREATED"
    assert rv.url == '/goals/4'

    rv = client.get('/goals/1')
    assert rv.status == "200 OK"


def test_goal_edit(client):
    rv = client.put('/goals/1/edit', data=dict({
                    'title': __title + "1",
                    'description': __description + "1",
                    'due_date': __duedate + timedelta(days=10)
                    }))
    assert rv.status == "204 NO_CONTENT"


def test_goal_delete(client):
    rv = client.delete('/goals/1')
    assert rv.status == "204 NO_CONTENT"
