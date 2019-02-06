def test_registration(client):
    _username = "SomeUserName"
    _email = "xxx@ttt.com"
    _firstname = "Ivan"
    _lastname = "Medvedev"
    _password = "Vodka"

    rv = client.get("/register")
    assert rv.status_code == 200
    assert "Register" in rv.data.decode()

    rv = client.post("/register", data=dict(
        username=_username,
        email=_email,
        firstname=_firstname,
        lastname=_lastname,
        password=_password,
        password2=_password), follow_redirects=True)

    assert rv.status_code == 200
    print(rv.data.decode())
    assert "Sign In" in rv.data.decode()

    rv = client.post("/login", data=dict(username=_username,
                                         password=_password),
                     follow_redirects=True)
    assert rv.status_code == 200
    assert "Logout" in rv.data.decode()

    rv = client.get("/logout", follow_redirects=True)

    assert rv.status_code == 200
    assert "Sign In" in rv.data.decode()
