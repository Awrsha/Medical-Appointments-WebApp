import os
import redis
from flask import g

REDIS_URL = os.getenv('REDIS_URL', 'redis://default:AWqlAAIjcDFlY2Y4NDQ3NzUzOTE0NmEwOGEzNTU0ZDkzNzE4ZmU2N3AxMA@cheerful-yak-27301.upstash.io:6379')

def get_db():
    if 'db' not in g:
        g.db = redis.from_url(REDIS_URL, ssl_cert_reqs=None)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        # No need to create tables in Redis

def query_db(key):
    db = get_db()
    return db.get(key)

def insert_db(key, value):
    db = get_db()
    db.set(key, value)

def get_all_appointments():
    db = get_db()
    keys = db.keys('appointment:*')
    return [db.get(key) for key in keys]