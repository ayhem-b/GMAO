# GMAO – Web-Based Maintenance Management System

A Django-based GMAO (Gestion de Maintenance Assistée par Ordinateur) platform designed to streamline industrial maintenance operations. This project integrates machine monitoring, work order management, fault reporting, and a live SCADA dashboard — aligning with Industry 4.0 principles.

---

## Features

-  **Intervention Management:** Submit, track, and visualize maintenance interventions.
-  **Admin Dashboard:** Real-time charts showing key maintenance KPIs (downtime, number of interventions, etc.).
-  **Machine Monitoring:** Track machine statuses live with visual indicators.
-  **Technician Portal:** Dedicated UI for maintenance technicians to submit and follow up on interventions.
-  **SCADA Integration:** Communicates with Siemens PLCs using Snap7 for real-time fault detection.
-  **SMS Alerts (via PLC):** Automatic notifications triggered by machine status changes.

---

## Tech Stack

- **Backend:** Django, Python  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Database:** PostgreSQL  
- **Communication:** Snap7 (for PLC connectivity)  
- **Deployment:** Local network (LAN)

---

## Project Structure
Not ready yet 

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ayhem-b/GMAO.git
   cd GMAO```
1. **Create virtual environment**
```python
python3 -m venv env
source env/bin/activate
```

1. **Install dependencies**
```python
pip install -r requirements.txt
```

1. **Run migrations**
```python
python manage.py migrate
```
1. **Create superuser (admin access)**
```python
python manage.py createsuperuser
```
1. **Start the server**
```python
python manage.py runserver
```
Then go to http://127.0.0.1:8000/ in your browser.

## PLC Communication

    Uses the Snap7 library to connect to Siemens S7-1200 PLCs.

    Real-time monitoring of machine states via Modbus-like data reads.

    Fault signals from the PLC automatically trigger UI alerts and database logs.

## Screenshots


    The admin dashboard

    The technician intervention form

    Machine status monitoring interface

## To Do

    Add authentication tokens for API endpoints

    Improve real-time update mechanism (currently uses periodic refresh)

    Export reports to PDF

    Dockerize for easier deployment

## Contributors

    Ayhem Belkhamsa – Developer and Project Lead

## License

This project is licensed under the MIT License.

_This project was developed as part of a capstone project in collaboration with Lear Corporation Tunisia, with the goal of digitizing industrial maintenance management and enhancing reactivity to machine faults._
