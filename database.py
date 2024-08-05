import os
import psycopg2
from flask import g, current_app

DATABASE_URL = "postgresql://postgres.uqsrxumceahdhoawdabx:Awrsha2559$@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id SERIAL PRIMARY KEY,
                specialty TEXT,
                doctor_id INTEGER,
                appointment_date DATE,
                appointment_time TIME,
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
