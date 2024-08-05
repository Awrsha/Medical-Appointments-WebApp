import sqlite3
from flask import g, Flask

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

def init_db():
    with sqlite3.connect(DATABASE) as db:
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
