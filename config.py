import os
class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or b'T\xd0\xc0\xeb\x14+\x85\xfa\xca\x90\xacE\x9d\xa7^~'