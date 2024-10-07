from flask import Flask, render_template, request, jsonify
from database import get_db, close_db, init_db
import json

app = Flask(__name__)

@app.route('/')
@app.route('/scheduling')
def home():
    return render_template('reserve.html')

@app.route('/check-availability')
def check_availability():
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    
    db = get_db()
    appointments = db.get(f'appointments:{doctor_id}:{date}')
    
    if appointments:
        booked_times = json.loads(appointments)
    else:
        booked_times = []
    
    return jsonify({"bookedTimes": booked_times})

@app.route('/submit-appointment', methods=['POST'])
def submit_appointment():
    appointment_data = request.json
    
    # Ensure all required fields are present
    required_fields = ['specialty', 'doctor_id', 'appointment_date', 'appointment_time',
                       'patient_name', 'phone_number', 'email', 'national_id',
                       'gender', 'insurance_type', 'medical_history']
    
    for field in required_fields:
        if field not in appointment_data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    db = get_db()
    
    # Generate a unique key for the appointment
    appointment_key = f"appointment:{appointment_data['doctor_id']}:{appointment_data['appointment_date']}:{appointment_data['appointment_time']}"
    
    # Store the appointment data
    db.set(appointment_key, json.dumps(appointment_data))
    
    # Update the list of booked times for this doctor and date
    booked_times_key = f"appointments:{appointment_data['doctor_id']}:{appointment_data['appointment_date']}"
    booked_times = db.get(booked_times_key)
    
    if booked_times:
        booked_times = json.loads(booked_times)
    else:
        booked_times = []
    
    booked_times.append(appointment_data['appointment_time'])
    db.set(booked_times_key, json.dumps(booked_times))
    
    return jsonify({"message": "Appointment successfully added"})

if __name__ == '__main__':
    init_db(app)
    app.run(port=5000, debug=True)