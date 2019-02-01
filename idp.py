from app import app, db 
from app.models import User, Goal

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Goal': Goal}