import requests

BASE_URL = 'http://127.0.0.1:8000'

def get_csrf(session):
    r = session.get(BASE_URL + '/admin/login')
    for line in r.text.split('\n'):
        if 'name="csrf_token"' in line:
            return line.split('value="')[1].split('"')[0]
    return ''

s = requests.Session()
csrf = get_csrf(s)

# Login
r_login = s.post(f"{BASE_URL}/admin/login", data={'username': 'admin', 'password': 'admin123', 'csrf_token': csrf})
print(f"Login status: {r_login.status_code}")

# Capture the authenticated session cookie
old_cookies = s.cookies.copy()
print("Captured session cookie.")

# Access dashboard to prove it works
r_dash = s.get(f"{BASE_URL}/admin/inquiries")
if "Inquiries" in r_dash.text:
    print("Dashboard accessible with current session.")

# Logout
s.get(f"{BASE_URL}/admin/logout")
print("Logged out.")

# Try to access dashboard after logout with the current session (which was cleared by the server's Set-Cookie)
r_after_logout = s.get(f"{BASE_URL}/admin/inquiries")
if r_after_logout.history and 'admin/login' in r_after_logout.url:
    print("Dashboard access denied (redirected to login) as expected.")

# Replay the old session cookie
s.cookies.update(old_cookies)
r_replay = s.get(f"{BASE_URL}/admin/inquiries")
if "Inquiries" in r_replay.text:
    print("VULNERABILITY CONFIRMED: Dashboard accessible by replaying old session cookie!")
else:
    print("Dashboard access denied. Session replay blocked.")
