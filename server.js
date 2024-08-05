const express = require('express');
const path = require('path');
const app = express();
const port = 5000;
const db = require('./database.js');

app.use(express.static(__dirname));
app.use(express.json());

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'reserve.html'));
});

app.get('/scheduling', (req, res) => {
    res.sendFile(path.join(__dirname, 'reserve.html'));
});

app.get('/check-availability', (req, res) => {
    const { doctor_id, date } = req.query;
    
    db.all(`SELECT appointment_time FROM appointments 
            WHERE doctor_id = ? AND appointment_date = ?`,
    [doctor_id, date], (err, rows) => {
        if (err) {
            console.error('Error checking availability', err.message);
            res.status(500).json({ error: 'Error checking availability' });
        } else {
            const bookedTimes = rows.map(row => row.appointment_time);
            res.status(200).json({ bookedTimes });
        }
    });
});

app.post('/submit-appointment', (req, res) => {
    const appointmentData = req.body;

    db.run(`INSERT INTO appointments (
        specialty, doctor_id, appointment_date, appointment_time,
        patient_name, phone_number, email, national_id,
        gender, insurance_type, medical_history
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    [
        appointmentData.specialty,
        appointmentData.doctor_id,
        appointmentData.appointment_date,
        appointmentData.appointment_time,
        appointmentData.patient_name,
        appointmentData.phone_number,
        appointmentData.email,
        appointmentData.national_id,
        appointmentData.gender,
        appointmentData.insurance_type,
        appointmentData.medical_history
    ], function(err) {
        if (err) {
            console.error('Error inserting appointment', err.message);
            res.status(500).json({ error: 'Error inserting appointment' });
        } else {
            console.log(`A new appointment has been added with rowid ${this.lastID}`);
            res.status(200).json({ message: 'Appointment successfully added' });
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});