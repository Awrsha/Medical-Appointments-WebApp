from flask import Flask, render_template, request, jsonify
from database import get_db, close_db, init_db

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
    cursor = db.cursor()
    cursor.execute("""
        SELECT appointment_time FROM appointments 
        WHERE doctor_id = ? AND appointment_date = ?
    """, (doctor_id, date))
    
    booked_times = [row[0] for row in cursor.fetchall()]
    return jsonify({"bookedTimes": booked_times})

@app.route('/submit-appointment', methods=['POST'])
def submit_appointment():
    appointment_data = request.json
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO appointments (
            specialty, doctor_id, appointment_date, appointment_time,
            patient_name, phone_number, email, national_id,
            gender, insurance_type, medical_history
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        appointment_data['specialty'],
        appointment_data['doctor_id'],
        appointment_data['appointment_date'],
        appointment_data['appointment_time'],
        appointment_data['patient_name'],
        appointment_data['phone_number'],
        appointment_data['email'],
        appointment_data['national_id'],
        appointment_data['gender'],
        appointment_data['insurance_type'],
        appointment_data['medical_history']
    ))
    db.commit()
    
    return jsonify({"message": "Appointment successfully added"})

if __name__ == '__main__':
    init_db(app)
    app.run(port=5000, debug=True)