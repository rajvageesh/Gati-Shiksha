# Gati Shiksha

Gati Shiksha is an educational initiative and platform designed to transform learning through STEM, digital literacy, and NEP-aligned pedagogical innovation. 

This repository contains the backend and frontend code for the official Gati Shiksha web platform. It is built using a modern **Python/Flask** backend, an **SQLite/SQLAlchemy** database, and a highly responsive, modern UI built with **Vanilla HTML5, CSS3, and JavaScript**.

## 🚀 Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite, Flask-SQLAlchemy
- **Frontend:** Vanilla HTML5, CSS3 (Glassmorphism & Modern UI), Vanilla JS
- **Environment Management:** python-dotenv

## 📂 Project Structure

- `app.py` - The main Flask application, routing, and form handling logic.
- `models.py` - SQLAlchemy database models (Programs, Mentors, Leaders, Metrics, Inquiries).
- `seed.py` - Database seed script to initialize required data.
- `extensions.py` - Flask extensions (e.g., SQLAlchemy instance).
- `templates/` - HTML files/Jinja2 templates (e.g., `base.html`, `index.html`).
- `static/` - Static assets (CSS, JS, and images).
- `instance/` - Contains the SQLite database file (`gatishiksha.db`).
- `requirements.txt` - Python dependencies.

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.8+ installed on your system.
- Git.

### 2. Clone the Repository
```bash
git clone https://github.com/rajvageesh/Gati-Shiksha.git
cd Gati-Shiksha
```

### 3. Create a Virtual Environment
```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: ensure `python-dotenv` is installed if running into import errors: `pip install python-dotenv`)*

### 5. Environment Variables
Create a `.env` file in the root directory and configure your mail server settings for the Contact form to work:
```env
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_app_password
```

### 6. Initialize the Database
Before running the app, you need to set up the database and seed it with initial data (Programs, Mentors, Metrics):
```bash
python seed.py
```
This will create `instance/gatishiksha.db` and populate it.

### 7. Run the Application
```bash
python app.py
```
The application will start running on `http://127.0.0.1:5000/`.

## 🌟 Key Features

- **Dynamic Data Rendering:** Programs, Advisory Network, Leadership, and Impact Metrics are fully dynamic and fetched from the SQLite database.
- **Modern Responsive Design:** A carefully crafted UI/UX with smooth transitions, glassmorphism overlays, and fully responsive layouts across all devices.
- **Core Services Carousel:** Infinite auto-sliding carousel built entirely with Vanilla JavaScript for maximum performance.
- **Contact Inquiry System:** Secure, backend-validated contact form that stores inquiries in the database and sends automated email notifications.

## 📄 License
This project is proprietary and confidential unless otherwise specified in the `LICENSE` file.
