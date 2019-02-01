from app import app, db, login
from app.models import User
from sqlalchemy.exc import IntegrityError
import pytest

__username="Jambo"
__email="xxx@xxx.com"
__firstname="John"
__lastname="Malcovic"
__password="Python"

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

def test_user_creation(db_connection):
	u = create_user(__username, __email, __password, __firstname, __lastname)

	users = User.query.all()
	assert len(users) == 1
	assert users[0].username == __username
	assert users[0].email == __email
	assert users[0].first_name == __firstname
	assert users[0].last_name == __lastname
	assert users[0] is not None

@pytest.mark.parametrize("username, email", [
    (None, __email),
    (__username, None),
])
def test_user_non_nullable(db_connection, username, email):
	with pytest.raises(IntegrityError):
		u = User(username=username, email=email)
		u.set_password(__password)
		db.session.add(u)
		db.session.commit()

def test_user_creation_without_pass(db_connection):
	with pytest.raises(IntegrityError):
		u = User(username=__username, email=__email, first_name=__firstname, last_name=__lastname)
		db.session.add(u)
		db.session.commit()

def test_repr(db_connection):
	u = create_user(__username, __email, __password, __firstname, __lastname)

	assert str(u) == '<User Jambo id=1>'

def create_user(username, email, password, firstname=None, lastname=None):
	u = User(username=username, email=email, first_name=firstname, last_name=lastname)
	u.set_password(password)

	db.session.add(u)
	db.session.commit()

	return u