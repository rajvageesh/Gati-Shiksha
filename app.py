from flask import Flask, render_template, request, redirect, url_for, flash, session

from extensions import db

from models import (
    Program,
    GatiShaala,
    Metric,
    Leader,
    Mentor,
    Inquiry
)
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from email_validator import validate_email, EmailNotValidError
import requests
import html
from datetime import timedelta, datetime


# =========================================
# LOAD ENVIRONMENT VARIABLES
# =========================================

load_dotenv()


# =========================================
# FLASK APPLICATION
# =========================================

app = Flask(__name__)
# Secret key securely loaded from environment variables
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "gati-shiksha-dev-secret-key-change-in-production")

# =========================================
# SERVER-SIDE SESSION TRACKING
# =========================================
# We maintain a set of active session IDs in memory.
# This prevents "Session Replay" attacks if a cookie is stolen, 
# because logout explicitly removes the ID from the server's tracking.
import uuid
active_sessions = set()

# =========================================
# SECURITY CONFIGURATION
# =========================================

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1 MB maximum request size
app.config['SESSION_COOKIE_SECURE'] = os.environ.get("FLASK_ENV") == "production"
app.config['SESSION_COOKIE_HTTPONLY'] = True    # Prevent JS access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # CSRF mitigation for cookies
csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning(f"Rate limit exceeded: {e.description} for IP: {get_remote_address()}")
    flash("Too many requests. Please try again later.", "error")
    return redirect(url_for('home') + "#contact")

@app.errorhandler(413)
def request_entity_too_large(e):
    logger.warning(f"Payload too large from IP: {get_remote_address()}")
    return "Request payload is too large. Please reduce the size of your input and try again.", 413

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal server error: {e}")
    return "An unexpected error occurred. Please try again later.", 500

@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

TURNSTILE_SITE_KEY = os.getenv("TURNSTILE_SITE_KEY")
TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY")

# =========================================
# EMAIL CONFIGURATION
# =========================================

MAIL_SERVER = os.getenv(
    "MAIL_SERVER"
)

MAIL_PORT = int(
    os.getenv(
        "MAIL_PORT",
        "587"
    )
)

MAIL_USERNAME = os.getenv(
    "MAIL_USERNAME"
)

MAIL_PASSWORD = os.getenv(
    "MAIL_PASSWORD"
)

MAIL_RECEIVER = os.getenv(
    "MAIL_RECEIVER"
)

# =========================================
# SEND INQUIRY EMAIL
# =========================================

import html

def send_inquiry_email(inquiry):

    message = MIMEMultipart(
        "alternative"
    )

    # =====================================
    # EMAIL HEADER
    # =====================================

    message["Subject"] = "New Gati Shiksha Inquiry"
    message["From"] = MAIL_USERNAME
    message["To"] = MAIL_RECEIVER
    
    # The inquiry.email has been strictly validated by email-validator (RFC 5322) 
    # preventing CRLF injection
    message.add_header("Reply-To", inquiry.email)


    # =====================================
    # HTML EMAIL CONTENT
    # =====================================

    html_content = f"""
    <html>

    <body>

        <h2>
            New Gati Shiksha Inquiry
        </h2>

        <p>
            A new inquiry has been submitted
            through the Gati Shiksha website.
        </p>

        <table
            border="1"
            cellpadding="10"
            cellspacing="0"
            style="
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
            "
        >

            <tr>

                <th align="left">
                    Field
                </th>

                <th align="left">
                    Information
                </th>

            </tr>


            <tr>

                <td>
                    Name
                </td>

                <td>
                    {html.escape(inquiry.name or "")}
                </td>

            </tr>


            <tr>

                <td>
                    Email
                </td>

                <td>
                    {html.escape(inquiry.email or "")}
                </td>

            </tr>


            <tr>

                <td>
                    Organisation
                </td>

                <td>
                    {html.escape(inquiry.organisation or "Not provided")}
                </td>

            </tr>


            <tr>

                <td>
                    Role
                </td>

                <td>
                    {html.escape(inquiry.role or "")}
                </td>

            </tr>


            <tr>

                <td>
                    Interested In
                </td>

                <td>
                    {html.escape(inquiry.program or "Not specified")}
                </td>

            </tr>


            <tr>

                <td>
                    Message
                </td>

                <td>
                    {html.escape(inquiry.message or "")}
                </td>

            </tr>


            <tr>

                <td>
                    Submitted At
                </td>

                <td>
                    {html.escape(str(inquiry.created_at or ""))}
                </td>

            </tr>

        </table>

    </body>

    </html>
    """


    # =====================================
    # CREATE HTML EMAIL
    # =====================================

    email_body = MIMEText(
        html_content,
        "html"
    )


    message.attach(
        email_body
    )


    # =====================================
    # CONNECT TO GMAIL
    # =====================================

    with smtplib.SMTP(
        MAIL_SERVER,
        MAIL_PORT
    ) as server:

        server.starttls()


        # =================================
        # LOGIN
        # =================================

        server.login(
            MAIL_USERNAME,
            MAIL_PASSWORD
        )


        # =================================
        # SEND EMAIL
        # =================================

        server.sendmail(
            MAIL_USERNAME,
            MAIL_RECEIVER,
            message.as_string()
        )
# =========================================
# DATABASE CONFIGURATION
# =========================================

db_url = os.getenv("DATABASE_URL", "sqlite:///gatishiksha.db")
# Convert legacy 'postgres://' to 'postgresql://' for SQLAlchemy compatibility
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



# =========================================
# INITIALIZE DATABASE
# =========================================

db.init_app(app)


# =========================================
# HOME ROUTE
# =========================================

@app.route("/")
def home():
    selected_program = request.args.get("program")
    programs = Program.query.all()

    gati_shaala = GatiShaala.query.all()

    metrics = Metric.query.all()

    leaders = Leader.query.all()

    mentors = [
        {
            "category": "Academic Advisors",
            "name": "Dr. Sanjay Kumar Pandey",
            "role": "Professor",
            "organization": "Jawaharlal Nehru University",
            "image": "images/mentors/advisor-1.png"
        },
        {
            "category": "Academic Advisors",
            "name": "Mr. Arun Kumar Mishra",
            "role": "Best Teaching Methodology Awarded",
            "organization": "NCERT",
            "image": "images/mentors/advisor-2.png"
        },
        {
            "category": "Education Experts",
            "name": "Mr. Khursheed Ahmed",
            "role": "President Awardee Teacher",
            "organization": None,
            "image": "images/mentors/advisor-3.png"
        },
        {
            "category": "Science & Technology Advisors",
            "name": "Mr. Raj Kumar Mishra",
            "role": "GEO Scientist",
            "organization": "Government of India",
            "image": "images/mentors/advisor-4.png"
        },
        {
            "category": "Science & Technology Advisors",
            "name": "Ms. Akanaksha Tripathi",
            "role": "GEO Scientist",
            "organization": "Government of India",
            "image": "images/mentors/advisor-5.png"
        }
    ]

    return render_template(
        "index.html",
        programs=programs,
        gati_shaala=gati_shaala,
        metrics=metrics,
        leaders=leaders,
        mentors=mentors,
        selected_program=selected_program,
        turnstile_site_key=TURNSTILE_SITE_KEY
    )

# =========================================
# PROGRAM DETAIL
# =========================================

@app.route("/program/<int:program_id>")
def program_detail(program_id):

    program = Program.query.get_or_404(program_id)

    return render_template(
        "program_detail.html",
        program=program
    )
# =========================================
# SUBMIT INQUIRY
# =========================================

@app.route("/submit-inquiry", methods=["POST"])
@limiter.limit("5 per minute; 20 per hour")
def submit_inquiry():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    organisation = request.form.get("organisation", "").strip()
    role = request.form.get("role", "").strip()
    message = request.form.get("message", "").strip()
    program = request.form.get("program", "").strip()

    # CAPTCHA Validation
    if TURNSTILE_SECRET_KEY:
        turnstile_response = request.form.get('cf-turnstile-response', '')
        if not turnstile_response:
            flash("Please complete the CAPTCHA.", "error")
            return redirect(url_for("home") + "#contact")
        
        verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        data = {
            'secret': TURNSTILE_SECRET_KEY,
            'response': turnstile_response,
            'remoteip': get_remote_address()
        }
        try:
            r = requests.post(verify_url, data=data, timeout=5)
            outcome = r.json()
            if not outcome.get('success'):
                logger.warning(f"CAPTCHA failed for IP: {get_remote_address()}")
                flash("CAPTCHA verification failed. Please try again.", "error")
                return redirect(url_for("home") + "#contact")
        except requests.exceptions.RequestException as e:
            logger.error(f"Turnstile verification error: {e}")
            flash("Service unavailable. Please try again later.", "error")
            return redirect(url_for("home") + "#contact")


    # =====================================
    # BASIC VALIDATION & LENGTH LIMITS
    # =====================================

    if not name or not email or not role or not message:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("home") + "#contact")

    if len(name) > 100 or len(email) > 254 or len(message) > 5000 or len(organisation) > 200 or len(role) > 150:
        logger.warning(f"Input length validation failed from {get_remote_address()}")
        flash("Input exceeds allowed length.", "error")
        return redirect(url_for("home") + "#contact")

    try:
        valid_email = validate_email(email)
        email = valid_email.email
    except EmailNotValidError as e:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("home") + "#contact")

    # =====================================
    # ANTI-ABUSE: DATABASE CHECKS
    # =====================================
    
    time_10_min_ago = datetime.utcnow() - timedelta(minutes=10)
    recent_inquiries = Inquiry.query.filter(
        Inquiry.email == email,
        Inquiry.created_at >= time_10_min_ago
    ).count()

    if recent_inquiries >= 3:
        logger.warning(f"Email rate limit exceeded for {email}")
        flash("Too many requests from this email. Please try again later.", "error")
        return redirect(url_for("home") + "#contact")

    time_1_min_ago = datetime.utcnow() - timedelta(minutes=1)
    duplicate_inquiry = Inquiry.query.filter(
        Inquiry.email == email,
        Inquiry.message == html.escape(message),
        Inquiry.created_at >= time_1_min_ago
    ).first()

    if duplicate_inquiry:
        logger.warning(f"Duplicate inquiry blocked for {email}")
        flash("This message was already submitted recently.", "error")
        return redirect(url_for("home") + "#contact")


    # =====================================
    # CREATE INQUIRY
    # =====================================

    inquiry = Inquiry(
        name=html.escape(name),
        email=email,
        organisation=html.escape(organisation),
        role=html.escape(role),
        message=html.escape(message),
        program=html.escape(program)
    )


    # =====================================
    # SAVE INQUIRY TO DATABASE
    # =====================================

    db.session.add(inquiry)
    db.session.commit()


    # =====================================
    # SEND EMAIL NOTIFICATION
    # =====================================

    try:
        send_inquiry_email(inquiry)
    except Exception as e:
        logger.error(f"Email sending failed: {e}")


    # =====================================
    # SUCCESS MESSAGE
    # =====================================

    flash("Your inquiry has been submitted successfully.", "success")

    return redirect(url_for("home") + "#contact")
# =========================================
# ADMIN LOGIN
# =========================================

@app.route("/admin/login", methods=["GET", "POST"])
@limiter.limit("5 per minute; 20 per hour")
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        # Temporary development credentials
        from werkzeug.security import check_password_hash
        ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "scrypt:32768:8:1$s2y2D03LSjz1FoQA$894a0bd6260ba7f241001995c900a69c828cede833a280412239b372b4e7c8a665b0a6af0a730ee81c010399c04a153ab4c1246706478a34416f37099106ad16")
        
        if username == "admin" and check_password_hash(ADMIN_PASSWORD_HASH, password):

            # Clear any pre-session state to prevent Session Fixation attacks
            session.clear()

            session["admin_logged_in"] = True
            
            # Generate and track a unique session ID
            session_id = str(uuid.uuid4())
            session["session_id"] = session_id
            active_sessions.add(session_id)

            return redirect(
                url_for("admin_inquiries")
            )


        flash(
            "Invalid username or password.",
            "error"
        )


    return render_template(
        "admin_login.html"
    )
# =========================================
# ADMIN INQUIRIES
# =========================================

@app.route("/admin/inquiries")
def admin_inquiries():

    if not session.get("admin_logged_in") or session.get("session_id") not in active_sessions:
        session.clear()
        return redirect(
            url_for("admin_login")
        )


    inquiries = Inquiry.query.order_by(
        Inquiry.created_at.desc()
    ).limit(200).all()


    return render_template(
        "admin_inquiries.html",
        inquiries=inquiries
    )

# =========================================
# UPDATE INQUIRY STATUS
# =========================================

@app.route(
    "/admin/inquiries/<int:inquiry_id>/status",
    methods=["POST"]
)
def update_inquiry_status(inquiry_id):

    # Check admin login and active session tracker
    if not session.get("admin_logged_in") or session.get("session_id") not in active_sessions:
        session.clear()
        return redirect(
            url_for("admin_login")
        )


    inquiry = Inquiry.query.get_or_404(
        inquiry_id
    )


    status = request.form.get(
        "status",
        "New"
    )


    allowed_statuses = [
        "New",
        "Contacted",
        "In Progress",
        "Closed"
    ]


    if status not in allowed_statuses:

        flash(
            "Invalid inquiry status.",
            "error"
        )

        return redirect(
            url_for("admin_inquiries")
        )


    inquiry.status = status

    db.session.commit()


    flash(
        "Inquiry status updated.",
        "success"
    )


    return redirect(
        url_for("admin_inquiries")
    )
# =========================================
# ADMIN LOGOUT
# =========================================

@app.route("/admin/logout")
def admin_logout():

    # Remove the session ID from the active tracker to prevent replay attacks
    session_id = session.get("session_id")
    if session_id in active_sessions:
        active_sessions.remove(session_id)

    session.clear()

    return redirect(
        url_for("admin_login")
    )

# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")