# -*- encoding: utf-8 -*-

import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from tools.config import Config
app = Flask(__name__)

db_config = Config().get('db')

class DBConfig:
	db_host = db_config['host']
	db_port = db_config['port']
	db_user = db_config['user']
	db_passwd = db_config['passwd']
	database = db_config['database']

	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (db_user, db_passwd, db_host, db_port, database)

	SQLALCHEMY_POOL_SIZE = 1024

	SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(DBConfig)
db = SQLAlchemy(app)



# redis
class RedisConfig:

	def __init__(self):
		redis_config = Config().get('redis')
		redis_host = redis_config['host']
		redis_port = redis_config['port']

		pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
		self.r = redis.Redis(connection_pool=pool)

	def add_data(self, key, data):
		pipe = self.r.pipeline()
		pipe.sadd(key, data)
		pipe.execute()

	def r_set(self, key, value, expire):
		self.r.set(key, value, ex=expire)

	def get_value(self, key):
		return self.r.get(key)

	def get_data(self, key):
		return self.r.spop(key)

	def count_data(self, key):
		return self.r.scard(key)

redis_cli = RedisConfig()
