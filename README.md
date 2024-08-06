# Online Doctor Appointment System

Welcome to the **Online Doctor Appointment System**. This project aims to streamline the process of booking medical appointments online. The system allows users to select a specialty, choose a doctor, pick an appointment date and time, and confirm the booking. This documentation will guide you through setting up and running the project.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- User-friendly interface for booking appointments
- Specialty and doctor selection
- Calendar integration for picking appointment dates
- Real-time appointment time slot availability
- Persian date picker integration
- Multi-step booking process with progress indicators

## Requirements
- Python 3.x
- Node.js
- Docker (for containerized deployment)
- Required Python and Node.js libraries (listed in `requirements.txt` and `package.json` respectively)

## Installation

### Using Docker

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Awrsha/Medical-Appointments-WebApp.git
   cd Medical-Appointments-WebApp
   ```

2. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

### Manual Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Awrsha/Medical-Appointments-WebApp.git
   cd Medical-Appointments-WebApp
   ```

2. **Set Up the Backend (Flask)**
   - Create a virtual environment and activate it
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - Install required Python packages
     ```bash
     pip install -r requirements.txt
     ```
   - Run the Flask server
     ```bash
     python server.py
     ```

3. **Set Up the Frontend (Node.js)**
   - Install Node.js packages
     ```bash
     npm install
     ```
   - Run the Node.js server
     ```bash
     node server.js
     ```

## Usage
### Running the Project

- **With Docker Compose**
  After running `docker-compose up --build`, the system will be accessible via:
  - Flask server at `http://localhost:5000`
  - Node.js server at `http://localhost:3000`

- **Manually**
  - Flask server: `http://localhost:5000`
  - Node.js server: `http://localhost:3000`

### Access the System
1. Open your web browser.
2. Navigate to `http://localhost:5000` for the Flask server.
3. Navigate to `http://localhost:3000` for the Node.js server.

## Project Structure
```
online-doctor-appointment-system/
├── database.py               # Database configuration and models
├── appointment_system.db
├── database.js               # Database configuration and models
├── docker-compose.yaml       # Docker Compose configuration
├── Dockerfile                # Dockerfile for the Flask server
├── requirements.txt          # Python dependencies
├── reserve.html              # HTML template for booking
├── server.py                 # Flask server code
├── server.js                 # Node.js server code
├── package.json              # Node.js dependencies
└── templates/                
    ├── reserve.html      
└── static/                
    └── css/
      ├── style.css
    └── js/
          ├── script.js

├── vercel.json & runtime.txt  # are just for Deploy on Vercel.com
```

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your forked repository.
5. Create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
