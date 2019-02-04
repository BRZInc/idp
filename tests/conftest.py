from app import app, db
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.models import User, Goal
import pytest

# @pytest.fixture
# def app():
#     app = create_app()
#     return app


@pytest.fixture()
def db_connection(request):
    # Setup test db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    db.create_all()

    def teardown_db():
        db.session.remove()
        db.drop_all()

    request.addfinalizer(teardown_db)
    return db


@pytest.fixture()
def client(db_connection):
    client = app.test_client()

    with app.app_context():
        init_db()
        login_user(client)

    yield client


def init_db():
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
              due_date=datetime.utcnow())
    g2 = Goal(title="Goal2", description="Description",
              due_date=datetime.utcnow() + relativedelta(months=1))
    g3 = Goal(title="Goal3", description="Description",
              due_date=datetime.utcnow() + relativedelta(months=2))

    u1.goals.append(g1)
    u1.goals.append(g2)
    u1.goals.append(g3)

    db.session.add_all([u1, u2, u3])

    db.session.commit()


def login_user(client):
    rv = client.post("/login", data=dict(username="User2",
                                         password="Password"))