#database for local
""" import sqlite3
from flask import g

DATABASE = 'appointment_system.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_db(e=None):
    db = g.pop('_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                specialty TEXT,
                doctor_id INTEGER,
                appointment_date TEXT,
                appointment_time TEXT,
                patient_name TEXT,
                phone_number TEXT,
                email TEXT,
                national_id TEXT,
                gender TEXT,
                insurance_type TEXT,
                medical_history TEXT
            )
        ''')
        db.commit() """

#database for vercel
import sqlite3
from flask import g

DATABASE = ':memory:'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_db(e=None):
    db = g.pop('_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                specialty TEXT,
                doctor_id INTEGER,
                appointment_date TEXT,
                appointment_time TEXT,
                patient_name TEXT,
                phone_number TEXT,
                email TEXT,
                national_id TEXT,
                gender TEXT,
                insurance_type TEXT,
                medical_history TEXT
            )
        ''')
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    db = get_db()
    db.execute(query, args)
    db.commit()