import os
import tempfile
import pytest

from idp import app


@pytest.fixture
def client():
    #db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    #flaskr.app.config['TESTING'] = True
    client = app.test_client()

    # with idp.app.app_context():
    #     idp.init_db()

    yield client

    # os.close(db_fd)
    # os.unlink(flaskr.app.config['DATABASE'])


def test_registration(client):
    _username = "SomeUserName"
    _email = "xxx@xxx.com"
    _firstname = "Ivan"
    _lastname = "Medvedev"
    _password = "Vodka"

    rv = client.post("/register", data=dict(
        username=_username,
        email=_email,
        firstname=_firstname,
        lastname=_lastname,
        password=_password))

    assert rv.status == "200 OK"

    rv = client.post("/login", data=dict(username=_username,
                                         password=_password))
    assert rv.status == "200 OK"

    rv = client.get("/logout", follow_redirects=True)

    assert rv.status == "200 OK"
