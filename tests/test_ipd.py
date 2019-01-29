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


def test_index(client):
    rv = client.get("/")
    assert rv.status == "200 OK"


def test_registration(client):
    _email = "xxx@xxx.com"
    _first_name = "Ivan"
    _last_name = "Medvedev"
    _password = "Vodka"

    rv = client.post("/registration", data=dict(email=_email,
                                                first_name=_first_name,
                                                last_name=_last_name,
                                                password=_password))
    assert rv.status == "200 OK"
    assert "Registration complete!" in rv.data

    rv = client.post("/login", data=dict(email=_email,
                                         password=_password))
    assert rv.status == "200 OK"
    assert "Welcome to Rastishka!" in rv.data

    rv = client.get("/logout", follow_redirects=True)
