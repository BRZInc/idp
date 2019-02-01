import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or b'T\xd0\xc0\xeb\x14+\x85\xfa\xca\x90\xacE\x9d\xa7^~'

	# Database
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	#Mailserver
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_SUPPORT = os.environ.get('MAIL_SUPPORT')
	# Set ADMINS variable in the following manner "set MAIL_ADMIN_EMAILS='xxx@xxx.com'"
	ADMINS=[os.environ.get('MAIL_ADMIN_EMAILS')]