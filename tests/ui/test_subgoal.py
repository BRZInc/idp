from datetime import datetime

# Subgoal tests
__title = "Some goal title"
__description = "Test description for the goal"
__duedate = datetime.utcnow()


def test_subgoal_list(client, log_user):
    rv = client.get('/goals/3', follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()

    assert "Subgoals" in data
    assert "Subgoal Test #1" in data
    assert "Subgoal Test #2" in data
    assert "Subgoal Test #3" in data


def test_subgoal_creation(client, log_user):
    rv = client.post('/goals/new', data=dict({
        'title': __title,
        'description': __description,
        'duedate': __duedate.strftime("%d.%m.%Y"),
        'subgoals-0-title': "Subgoal #1",
        'subgoals-0-duedate': '',
        'subgoals-1-title': "Subgoal #2",
        'subgoals-1-duedate': '',
        'subgoals-2-title': "Subgoal #3",
        'subgoals-2-duedate': ''
    }), follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    print(data)

    assert "Subgoals" in data
    assert "Subgoal #1" in data
    assert "Subgoal #2" in data
    assert "Subgoal #3" in data


def test_subgoal_creation_long_title(client, log_user):
    length = 141

    rv = client.post('/goals/new', data=dict({
        'title': __title,
        'description': __description,
        'duedate': __duedate.strftime("%d.%m.%Y"),
        'subgoals-0-title': "A" * length,
        'subgoals-0-duedate': __duedate.strftime("%d.%m.%Y")
    }), follow_redirects=True)

    assert rv.status_code == 200

    data = rv.data.decode()
    # Check that we stay on the same page, but received an error message
    assert "Create New Goal" in data
    assert "Field must be between 1 and 140 characters long." in data


def test_subgoal_creation_1000(client, log_user):
    d = dict({
        'title': __title,
        'description': __description,
        'duedate': __duedate.strftime("%d.%m.%Y")
    })

    for n in range(0, 101):
        d["subgoals-{}-title".format(n)] = "Subgoal #{}".format(n)
        d["subgoals-{}-duedate".format(n)] = __duedate.strftime("%d.%m.%Y")

    rv = client.post('/goals/new', data=d, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    from re import findall

    assert len(findall('Subgoal #', data)) == 100


def test_subgoal_creation_validation_errors(client, log_user):
    rv = client.post('/goals/new', data=dict({
        'title': __title,
        'description': __description,
        'duedate': __duedate.strftime("%d.%m.%Y"),
        'subgoals-0-title': ''
    }), follow_redirects=True)

    print(rv.data.decode())

    assert rv.status_code == 200
    data = rv.data.decode()
    # Check that we stay on the same page, but received an error message
    assert "Create New Goal" in data
    assert "Field  is required" in rv.data.decode()


def test_subgoal_editing(client, log_user):
    rv = client.post('/goals/new', data=dict({
        'title': __title,
        'description': __description,
        'duedate': __duedate.strftime("%d.%m.%Y"),
        'subgoals-0-title': "Subgoal #1",
        'subgoals-0-duedate': '',
        'subgoals-1-title': "Subgoal #2",
        'subgoals-1-duedate': '',
        'subgoals-2-title': "Subgoal #3",
        'subgoals-2-duedate': ''
    }), follow_redirects=True)

    assert rv.status_code == 200

    rv = client.post('/goals/4/edit', data=dict({
        'title': __title,
        'description': __description,
        'duedate': __duedate.strftime("%d.%m.%Y"),
        'subgoals-0-title': "Subgoal #1 new name",
        'subgoals-0-duedate': __duedate.strftime("%d.%m.%Y"),
        'subgoals-1-title': "Subgoal #2",
        'subgoals-1-duedate': __duedate.strftime("%d.%m.%Y")
    }), follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert "Subgoal new name" in data
    assert "Subgoal #2" in data
    assert "Subgoal #3" not in data

    data = rv.data.decode()
    from re import findall

    assert len(findall('Subgoal #', data)) == 2


def test_subgoal_deletion(client, log_user):
    rv = client.post('/goals/new', data=dict({
        'title': __title,
        'description': __description,
        'duedate': __duedate.strftime("%d.%m.%Y"),
        'subgoals': (
            {
                'title': "Subgoal #1",
                'duedate': __duedate.strftime("%d.%m.%Y")
            },
            {
                'title': "Subgoal #2",
                'duedate': __duedate.strftime("%d.%m.%Y")
            },
            {
                'title': "Subgoal #3"
            }
        )
    }), follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()

    #TODO: check how to test deletion of the subgoals

    assert "Subgoal #" not in data

    raise NotImplementedError()
