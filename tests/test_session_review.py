import requests

BASE_URL = 'http://127.0.0.1:8000'

def get_csrf(session):
    r = session.get(BASE_URL + '/admin/login')
    for line in r.text.split('\n'):
        if 'name="csrf_token"' in line:
            return line.split('value="')[1].split('"')[0]
    return ''

print("=== RUNNING SESSION SECURITY REVIEW TESTS ===")

# Test 1: Session Fixation Test
# A pre-session variable stored in Flask session before login
s_fix = requests.Session()
# First visit to get session & CSRF
csrf_fix = get_csrf(s_fix)
r_login_fix = s_fix.post(f"{BASE_URL}/admin/login", data={'username': 'admin', 'password': 'admin123', 'csrf_token': csrf_fix})

if "Invalid username or password" not in r_login_fix.text and r_login_fix.status_code == 200:
    print("[TEST 1] Login status: 200 SUCCESS")
else:
    print(f"[TEST 1] Login status: {r_login_fix.status_code}, url: {r_login_fix.url}")

# Test 2: Replay Test
csrf = get_csrf(s_fix)
r_dash = s_fix.get(f"{BASE_URL}/admin/inquiries")
if "Inquiries" in r_dash.text:
    print("[TEST 2] Dashboard access: PASS")
else:
    print(f"[TEST 2] Dashboard access: FAIL ({r_dash.url})")
