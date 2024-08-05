const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('./appointment_system.db', (err) => {
    if (err) {
        console.error('Error opening database', err.message);
    } else {
        console.log('Connected to the appointment database.');
        initializeDatabase();
    }
});

function initializeDatabase() {
    db.get(`SELECT name FROM sqlite_master WHERE type='table' AND name='appointments'`, (err, row) => {
        if (err) {
            console.error('Error checking for table existence', err.message);
        } else if (row) {
            console.log('Appointments table already exists.');
        } else {
            createNewTable();
        }
    });
}

function createNewTable() {
    db.run(`CREATE TABLE appointments (
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
    )`, (err) => {
        if (err) {
            console.error('Error creating table', err.message);
        } else {
            console.log('New appointments table created successfully.');
        }
    });
}

module.exports = db;