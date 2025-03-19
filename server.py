from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import json
import time
import logging
from datetime import datetime, timedelta
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = "https://umpoltpdmdjgyhyvgxeu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVtcG9sdHBkbWRqZ3loeXZneGV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzEwNzU4MDksImV4cCI6MjA0NjY1MTgwOX0.MwVqnRoSJwg_r6DhJcIFs8oJHhs9KiJ4wkiV_9Dnq9Q"

# Create a connection pool with timeout settings
def get_supabase_client() -> Client:
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY, options={
            'timeout': 5,  # 5 seconds timeout
            'retries': 1   # Only retry once
        })
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {str(e)}")
        return None

# Cache for offline data
cache = {
    'appointments': {},
    'last_updated': None
}

# Offline fallback data
def get_offline_booked_times(doctor_id, date):
    """Generate consistent fake booked times for offline mode."""
    # Use doctor_id and date to generate a consistent set of booked times
    random.seed(f"{doctor_id}_{date}")
    all_times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
                "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
    
    # Randomly select 2-4 time slots as booked
    num_booked = random.randint(2, 4)
    return random.sample(all_times, num_booked)

@app.route('/')
@app.route('/scheduling')
def home():
    return render_template('reserve.html')

@app.route('/check-availability')
def check_availability():
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    
    if not doctor_id or not date:
        return jsonify({"error": "Missing required parameters"}), 400
    
    # Try to get data from Supabase
    try:
        supabase = get_supabase_client()
        if not supabase:
            raise Exception("Could not connect to Supabase")
        
        # Set a timeout for the request
        start_time = time.time()
        response = supabase.table('appointments')\
            .select('appointment_time')\
            .eq('doctor_id', doctor_id)\
            .eq('appointment_date', date)\
            .execute()
        
        # Update cache with fresh data
        cache_key = f"{doctor_id}_{date}"
        booked_times = [record['appointment_time'] for record in response.data]
        cache['appointments'][cache_key] = booked_times
        cache['last_updated'] = datetime.now()
        
        logger.info(f"Successfully retrieved booked times for doctor {doctor_id} on {date}")
        return jsonify({"bookedTimes": booked_times})
    
    except Exception as e:
        logger.error(f"Error checking availability: {str(e)}")
        
        # Check if we have cached data
        cache_key = f"{doctor_id}_{date}"
        if cache_key in cache['appointments'] and cache['last_updated'] and \
           (datetime.now() - cache['last_updated']) < timedelta(hours=1):
            # Use cached data if it's less than 1 hour old
            logger.info(f"Using cached data for doctor {doctor_id} on {date}")
            return jsonify({"bookedTimes": cache['appointments'][cache_key], "fromCache": True})
        else:
            # Fallback to offline data
            logger.info(f"Using offline data for doctor {doctor_id} on {date}")
            offline_booked_times = get_offline_booked_times(doctor_id, date)
            return jsonify({"bookedTimes": offline_booked_times, "offline": True})

@app.route('/submit-appointment', methods=['POST'])
def submit_appointment():
    appointment_data = request.json
    
    # Validate required fields
    required_fields = ['doctor_id', 'appointment_date', 'appointment_time', 'patient_name', 
                      'phone_number', 'email', 'national_id', 'gender', 'insurance_type']
    
    for field in required_fields:
        if field not in appointment_data or not appointment_data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        # Try to submit to Supabase
        supabase = get_supabase_client()
        if not supabase:
            raise Exception("Could not connect to Supabase")
        
        response = supabase.table('appointments').insert({
            'specialty': appointment_data.get('specialty', ''),
            'doctor_id': appointment_data['doctor_id'],
            'appointment_date': appointment_data['appointment_date'],
            'appointment_time': appointment_data['appointment_time'],
            'patient_name': appointment_data['patient_name'],
            'phone_number': appointment_data['phone_number'],
            'email': appointment_data['email'],
            'national_id': appointment_data['national_id'],
            'gender': appointment_data['gender'],
            'insurance_type': appointment_data['insurance_type'],
            'medical_history': appointment_data.get('medical_history', '')
        }).execute()
        
        # Update local cache to include this appointment
        cache_key = f"{appointment_data['doctor_id']}_{appointment_data['appointment_date']}"
        if cache_key in cache['appointments']:
            cache['appointments'][cache_key].append(appointment_data['appointment_time'])
        else:
            cache['appointments'][cache_key] = [appointment_data['appointment_time']]
        
        logger.info(f"Successfully added appointment for {appointment_data['patient_name']}")
        return jsonify({"message": "Appointment successfully added", "id": response.data[0]['id'] if response.data else None})
    
    except Exception as e:
        logger.error(f"Error submitting appointment: {str(e)}")
        
        # Store in local file as fallback
        try:
            offline_dir = "offline_data"
            if not os.path.exists(offline_dir):
                os.makedirs(offline_dir)
            
            offline_file = os.path.join(offline_dir, "pending_appointments.json")
            
            # Read existing data
            pending_appointments = []
            if os.path.exists(offline_file):
                with open(offline_file, 'r') as f:
                    try:
                        pending_appointments = json.load(f)
                    except json.JSONDecodeError:
                        pending_appointments = []
            
            # Add timestamp for syncing later
            appointment_data['created_at'] = datetime.now().isoformat()
            appointment_data['synced'] = False
            
            # Append new appointment
            pending_appointments.append(appointment_data)
            
            # Write back to file
            with open(offline_file, 'w') as f:
                json.dump(pending_appointments, f, indent=2)
            
            # Update local cache to include this appointment
            cache_key = f"{appointment_data['doctor_id']}_{appointment_data['appointment_date']}"
            if cache_key in cache['appointments']:
                cache['appointments'][cache_key].append(appointment_data['appointment_time'])
            else:
                cache['appointments'][cache_key] = [appointment_data['appointment_time']]
            
            logger.info(f"Saved appointment to offline storage for {appointment_data['patient_name']}")
            return jsonify({"message": "Appointment stored locally for later synchronization", "offline": True})
        
        except Exception as write_err:
            logger.error(f"Error saving appointment to offline storage: {str(write_err)}")
            return jsonify({"error": "Could not save appointment data. Please try again."}), 500

@app.route('/api/specialties')
def get_specialties():
    """Endpoint to get all specialties (offline data)"""
    specialties = [
        {"id": "cardiology", "name": "قلب و عروق", "icon": "fa-heartbeat"},
        {"id": "neurology", "name": "مغز و اعصاب", "icon": "fa-brain"},
        {"id": "orthopedics", "name": "ارتوپدی", "icon": "fa-bone"},
        {"id": "dentistry", "name": "دندانپزشکی", "icon": "fa-tooth"},
        {"id": "ophthalmology", "name": "چشم پزشکی", "icon": "fa-eye"},
        {"id": "dermatology", "name": "پوست و مو", "icon": "fa-allergies"}
    ]
    return jsonify(specialties)

@app.route('/api/doctors')
def get_doctors():
    """Endpoint to get doctors by specialty (offline data)"""
    specialty = request.args.get('specialty')
    
    all_doctors = {
        "cardiology": [
            {"id": 1, "name": "دکتر محمد حسینی", "expertise": "متخصص قلب", "image": "https://i.imgur.com/zVGddRs.jpg"},
            {"id": 2, "name": "دکتر سارا کریمی", "expertise": "فوق تخصص آریتمی قلب", "image": "https://i.imgur.com/zURjRt5.jpg"}
        ],
        "neurology": [
            {"id": 3, "name": "دکتر علی رضایی", "expertise": "متخصص مغز و اعصاب", "image": "https://i.imgur.com/yJeNlLI.jpg"},
            {"id": 4, "name": "دکتر فاطمه موسوی", "expertise": "فوق تخصص جراحی مغز", "image": "https://i.imgur.com/Y1xoVqD.jpg"}
        ],
        "orthopedics": [
            {"id": 5, "name": "دکتر امیر احمدی", "expertise": "متخصص ارتوپدی", "image": "https://i.imgur.com/yDqP4V6.jpg"},
            {"id": 6, "name": "دکتر مینا نادری", "expertise": "فوق تخصص جراحی زانو", "image": "https://i.imgur.com/3TLn1hd.jpg"}
        ],
        "dentistry": [
            {"id": 7, "name": "دکتر رضا محمدی", "expertise": "دندانپزشک عمومی", "image": "https://i.imgur.com/RfvFFBl.jpg"},
            {"id": 8, "name": "دکتر نیلوفر صادقی", "expertise": "متخصص ارتودنسی", "image": "https://i.imgur.com/BVtlxvT.jpg"}
        ],
        "ophthalmology": [
            {"id": 9, "name": "دکتر ناصر جعفری", "expertise": "متخصص چشم", "image": "https://i.imgur.com/3ZCHrWH.jpg"},
            {"id": 10, "name": "دکتر زهرا حبیبی", "expertise": "فوق تخصص قرنیه", "image": "https://i.imgur.com/1EQNPQW.jpg"}
        ],
        "dermatology": [
            {"id": 11, "name": "دکتر مهدی تهرانی", "expertise": "متخصص پوست و مو", "image": "https://i.imgur.com/T1G9Rch.jpg"},
            {"id": 12, "name": "دکتر لیلا کاظمی", "expertise": "متخصص زیبایی پوست", "image": "https://i.imgur.com/YFFA9sQ.jpg"}
        ]
    }
    
    if specialty and specialty in all_doctors:
        return jsonify(all_doctors[specialty])
    
    # If no specialty is specified or invalid specialty, return all doctors
    return jsonify(all_doctors)

@app.route('/service-worker.js')
def service_worker():
    """Serve the service worker for offline capabilities"""
    return app.send_static_file('service-worker.js')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('reserve.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error. The system is currently experiencing issues."}), 500

if __name__ == '__main__':
    # Create offline data directory if it doesn't exist
    offline_dir = "offline_data"
    if not os.path.exists(offline_dir):
        os.makedirs(offline_dir)
    
    app.run(port=5000, debug=True)