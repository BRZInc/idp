from app import app, db
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from app.models import User, Goal, Subgoal
import pytest

# Sample user data
__username = "ConanArny"
__email = "conan@schwarzenegger.com"
__password = "I'mTheArny"

# Sample goal data
__title = "Coach my Abs"
__description = "Some good things to mention here"
__duedate = datetime.utcnow() + timedelta(days=30)


@pytest.fixture()
def dbc(request):
    # Setup test db
    db.drop_all()
    db.create_all()

    def teardown_db():
        db.session.remove()
        db.drop_all()

    request.addfinalizer(teardown_db)
    return db


@pytest.fixture(scope="class")
def client():
    print("Setting app settings")
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['WTF_CSRF_ENABLED'] = False

    client = app.test_client()

    with app.app_context():
        init_db()

    yield client


def init_db():
    print("Start db init")
    db.session.remove()
    db.drop_all()
    db.create_all()

    u1 = User(username="User1", first_name="Ivan",
              last_name="Fedorovsky", email="ivan.fedorovsky@xyz.com")
    u2 = User(username="User2", first_name="Dzimurhan",
              last_name="Zaliphan", email="dz@xyz.com")
    u3 = User(username="User3", first_name="Zope",
              last_name="Zope", email="zope_zope@xyz.com")
    u1.set_password('Password')
    u2.set_password('Password')
    u3.set_password('Password')

    g1 = Goal(title="Goal1", description="Description",
              duedate=datetime.utcnow())
    g2 = Goal(title="Goal2", description="Description",
              duedate=datetime.utcnow() + relativedelta(months=1))
    g3 = Goal(title="Goal3", description="Description",
              duedate=datetime.utcnow() + relativedelta(months=2))

    s1 = Subgoal(title="Subgoal Test #1", duedate=datetime.utcnow())
    s2 = Subgoal(title="Subgoal Test #2")
    s3 = Subgoal(title="Subgoal Test #3")

    g3.subgoals.append(s1)
    g3.subgoals.append(s2)
    g3.subgoals.append(s3)

    u1.goals.append(g1)
    u1.goals.append(g2)
    u1.goals.append(g3)

    db.session.add_all([u1, u2, u3])

    db.session.commit()

    assert User.query.count() == 3

    print("Finish db init")


@pytest.fixture(scope="class")
def log_user(client):
    print("Logging User 2 in")
    rv = client.post("/login", data=dict(username="User2",
                                         password="Password"),
                     follow_redirects=True)

    assert rv.status_code == 200
    print("Logged User 2 in")


@pytest.fixture()
def test_user(dbc):
    u = User(username=__username, email=__email)
    u.set_password(__password)

    dbc.session.add(u)
    dbc.session.commit()

    return u


@pytest.fixture()
def test_goal(dbc, test_user):
    g = create_goal(dbc, __title, test_user.id, __description, __duedate)
    return g


def create_goal(db, title, user_id, description=None, duedate=None):
    goal = Goal(title=title, user_id=user_id,
                description=description, duedate=duedate)

    db.session.add(goal)
    db.session.commit()
    return goal
