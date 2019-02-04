import os
import tempfile
import pytest

from idp import app

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
