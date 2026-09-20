# GovBus – Local Bus Ticket Booking System

“Simple. Smart. Connected.”

GovBus is a professional, full-stack web application built with Python and Django. It provides a platform for passengers to search, select seats, and book tickets for local public transportation. This is a demonstration/academic project showcasing a realistic public transit booking system.

## Features

**For Passengers:**
- Modern, responsive User Interface using Bootstrap 5.
- User registration, login, and profile management.
- Dynamic bus schedule search.
- Interactive seat selection map.
- Complete booking flow with demo payment confirmation.
- Digital Ticket generation with functional QR codes.
- Booking history and dashboard.
- Cancellation functionality.

**For Administrators:**
- Comprehensive Django Admin dashboard to manage buses, routes, schedules, stops, and bookings.
- Search and filter capabilities for managing records efficiently.

## Tech Stack
- **Backend:** Python 3, Django 4.2
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript, Bootstrap Icons
- **Database:** SQLite (PostgreSQL-ready)
- **Additional:** `qrcode` and `Pillow` for ticket QR generation.

## Installation and Setup

### Prerequisites
- Python 3.8+ installed on your system.

### Steps
1. **Clone or Download the Repository:**
   Navigate to the project directory in your terminal.

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Load Demo Data (Optional but Recommended):**
   This populates the database with sample buses, routes, and schedules for the next 7 days.
   ```bash
   python manage.py load_demo_data
   ```

7. **Create a Superuser (Admin):**
   If you didn't run the automated setup above, create one manually:
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Demo Credentials
- **Admin Dashboard:** `http://127.0.0.1:8000/admin/`
- **Username:** `admin`
- **Password:** `admin123`

## How the Booking Flow Works
1. **Search:** The user enters a source, destination, and travel date on the homepage.
2. **Select Bus:** Available schedules matching the search are displayed with departure times, fares, and available seats.
3. **Select Seat:** The user is presented with a visual 2x2 seat map of the bus. They can click to select any available seat (green). Booked seats are disabled (red).
4. **Confirm & Book:** After selecting a seat, the user provides passenger details and clicks confirm. The system deducts from the available seats counter and creates a `Booking` record.
5. **Ticket Generation:** A `Ticket` record is immediately created, and a QR Code containing journey data is generated and saved locally. The user is redirected to view their digital ticket.

## Disclaimer
This is an academic/demo project. It is not affiliated with any official government entity. All routes, schedules, and data are fictional. No real payment gateways are integrated.
