from flask import Flask, render_template, request, jsonify
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = "https://umpoltpdmdjgyhyvgxeu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVtcG9sdHBkbWRqZ3loeXZneGV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEwNzU4MDksImV4cCI6MjA0NjY1MTgwOX0.MwVqnRoSJwg_r6DhJcIFs8oJHhs9KiJ4wkiV_9Dnq9Q"

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
@app.route('/scheduling')
def home():
    return render_template('reserve.html')

@app.route('/check-availability')
def check_availability():
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    
    response = supabase.table('appointments')\
        .select('appointment_time')\
        .eq('doctor_id', doctor_id)\
        .eq('appointment_date', date)\
        .execute()
    
    booked_times = [record['appointment_time'] for record in response.data]
    return jsonify({"bookedTimes": booked_times})

@app.route('/submit-appointment', methods=['POST'])
def submit_appointment():
    appointment_data = request.json
    
    try:
        response = supabase.table('appointments').insert({
            'specialty': appointment_data['specialty'],
            'doctor_id': appointment_data['doctor_id'],
            'appointment_date': appointment_data['appointment_date'],
            'appointment_time': appointment_data['appointment_time'],
            'patient_name': appointment_data['patient_name'],
            'phone_number': appointment_data['phone_number'],
            'email': appointment_data['email'],
            'national_id': appointment_data['national_id'],
            'gender': appointment_data['gender'],
            'insurance_type': appointment_data['insurance_type'],
            'medical_history': appointment_data['medical_history']
        }).execute()
        
        return jsonify({"message": "Appointment successfully added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)