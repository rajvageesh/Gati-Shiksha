import requests
import time
from email_validator import validate_email, EmailNotValidError

BASE_URL = 'http://127.0.0.1:8000'

def get_csrf(session):
    r = session.get(BASE_URL + '/')
    for line in r.text.split('\n'):
        if 'name="csrf_token"' in line:
            return line.split('value="')[1].split('"')[0]
    return ''

print("=== STARTING SECURITY TESTS ===")

s = requests.Session()

# 1. CSRF Missing
print("\n[TEST] Missing CSRF Token")
r = s.post(f"{BASE_URL}/submit-inquiry", data={"name": "Test"})
print(f"Status: {r.status_code} (Expected 400)")

# Get valid CSRF
csrf = get_csrf(s)
print(f"Got CSRF: {csrf[:10]}...")

# 2. Missing Fields
print("\n[TEST] Missing Fields")
r = s.post(f"{BASE_URL}/submit-inquiry", data={"csrf_token": csrf})
# Flask redirects with 302 on validation error (flash message), let's check history
print(f"Status: {r.status_code}")
if r.history:
    print(f"Redirected from: {r.history[0].status_code}")

# 3. Invalid Email
print("\n[TEST] Invalid Email")
r = s.post(f"{BASE_URL}/submit-inquiry", data={
    "csrf_token": csrf,
    "name": "Test",
    "email": "invalid_email",
    "role": "Teacher",
    "message": "Test message"
})
print(f"Status: {r.status_code}")
if r.history:
    print(f"Redirected from: {r.history[0].status_code}")

# 4. Oversized fields
print("\n[TEST] Oversized Fields")
r = s.post(f"{BASE_URL}/submit-inquiry", data={
    "csrf_token": csrf,
    "name": "A" * 150,
    "email": "test@example.com",
    "role": "Teacher",
    "message": "Test"
})
print(f"Status: {r.status_code}")
if r.history:
    print(f"Redirected from: {r.history[0].status_code}")

# 5. Oversized Request (413)
print("\n[TEST] Oversized Payload (413)")
large_payload = "A" * (2 * 1024 * 1024) # 2MB
try:
    r = s.post(f"{BASE_URL}/submit-inquiry", data={
        "csrf_token": csrf,
        "message": large_payload
    })
    print(f"Status: {r.status_code} (Expected 413)")
except requests.exceptions.ConnectionError:
    print("Connection closed by server (Expected for 413)")

# 6. Admin Login Brute Force with CSRF
print("\n[TEST] Admin Login Brute Force with valid CSRF")
# Get valid CSRF token from admin login page
s_admin = requests.Session()
r_admin = s_admin.get(f"{BASE_URL}/admin/login")
admin_csrf = ''
for line in r_admin.text.split('\n'):
    if 'name="csrf_token"' in line:
        admin_csrf = line.split('value="')[1].split('"')[0]
        break

print(f"Got Admin CSRF: {admin_csrf[:10]}...")

# 6a. Invalid Login
r = s_admin.post(f"{BASE_URL}/admin/login", data={"username": "admin", "password": "wrong", "csrf_token": admin_csrf})
print(f"Invalid Login Status: {r.status_code}")
if r.history:
    print(f"Invalid Login Redirect: {r.history[0].status_code} to {r.url}")

# 6b. Valid Login
r_login = s_admin.post(f"{BASE_URL}/admin/login", data={"username": "admin", "password": "admin123", "csrf_token": admin_csrf})
print(f"Valid Login Status: {r_login.status_code}")
if r_login.history:
    print(f"Valid Login Redirect: {r_login.history[0].status_code} to {r_login.url}")

# 6c. Verify we can access inquiries
r_inquiries = s_admin.get(f"{BASE_URL}/admin/inquiries")
print(f"Inquiries Page Status: {r_inquiries.status_code}")
if "Inquiries" in r_inquiries.text:
    print("Successfully accessed Admin Inquiries dashboard.")

# 6d. Test Inquiry Management (Update Status)
# First we need to get an inquiry ID from the inquiries page and the CSRF token
inquiries_csrf = ''
inquiry_id = None
for line in r_inquiries.text.split('\n'):
    if 'name="csrf_token"' in line:
        inquiries_csrf = line.split('value="')[1].split('"')[0]
    if 'action="/admin/inquiries/' in line:
        inquiry_id = line.split('action="/admin/inquiries/')[1].split('/status')[0]
    if inquiries_csrf and inquiry_id:
        break

if inquiry_id:
    print(f"Found inquiry ID: {inquiry_id}")
    # 6d.1 Missing CSRF
    r_status_fail = s_admin.post(f"{BASE_URL}/admin/inquiries/{inquiry_id}/status", data={"status": "Closed"})
    print(f"Update Status Missing CSRF: {r_status_fail.status_code} (Expected 400)")

    # 6d.2 Valid CSRF
    r_status_success = s_admin.post(f"{BASE_URL}/admin/inquiries/{inquiry_id}/status", data={"status": "Closed", "csrf_token": inquiries_csrf})
    print(f"Update Status Valid CSRF: {r_status_success.status_code}")
    if r_status_success.history:
        print(f"Update Status Redirect: {r_status_success.history[0].status_code} to {r_status_success.url}")
else:
    print("No inquiries found to test status update.")


print("\n[TEST] Submit Inquiry Rate Limit")
for i in range(7):
    r = s.post(f"{BASE_URL}/submit-inquiry", data={"csrf_token": csrf, "name": "test", "email": "a@b.c", "role": "T", "message": "hello", "program": ""})
    print(f"Attempt {i+1}: {r.status_code}")
    if r.history:
        print(f"Redirected from: {r.history[0].status_code} to {r.url}")
        if "Too many requests" in r.text:
            print("Found Rate Limit flash message in response.")
        elif "already submitted recently" in r.text:
            print("Found Anti-spam flash message in response.")


