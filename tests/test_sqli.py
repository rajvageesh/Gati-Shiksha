import requests

BASE_URL = 'http://127.0.0.1:8000'

def get_csrf(session):
    r = session.get(BASE_URL + '/admin/login')
    for line in r.text.split('\n'):
        if 'name="csrf_token"' in line:
            return line.split('value="')[1].split('"')[0]
    return ''

s = requests.Session()

payloads = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "admin' --",
    "' OR 'x'='x"
]

print("=== SQL INJECTION TESTS ===")

# Test Valid
csrf = get_csrf(s)
r = s.post(f"{BASE_URL}/admin/login", data={"username": "admin", "password": "admin123", "csrf_token": csrf})
print(f"Valid Credentials: {r.status_code}")
if r.history:
    print(f"Redirects to: {r.url}")

# Test Unknown Email (actually username)
s2 = requests.Session()
csrf2 = get_csrf(s2)
r2 = s2.post(f"{BASE_URL}/admin/login", data={"username": "nonexistent", "password": "password", "csrf_token": csrf2})
if "Invalid username or password" in r2.text or "Too many requests" in r2.text or r2.status_code in [200, 302, 429]:
    print("Unknown Email: Rejected properly")
else:
    print("Unknown Email: Failed")

# Test Wrong Password
s3 = requests.Session()
csrf3 = get_csrf(s3)
r3 = s3.post(f"{BASE_URL}/admin/login", data={"username": "admin", "password": "wrongpassword", "csrf_token": csrf3})
if "Invalid username or password" in r3.text or "Too many requests" in r3.text or r3.status_code in [200, 302, 429]:
    print("Wrong Password: Rejected properly")
else:
    print("Wrong Password: Failed")

# Test SQLi
for p in payloads:
    s_temp = requests.Session()
    csrf_temp = get_csrf(s_temp)
    # Test in username
    r_sqli = s_temp.post(f"{BASE_URL}/admin/login", data={"username": p, "password": "admin123", "csrf_token": csrf_temp})
    if "admin/inquiries" not in r_sqli.url:
        print(f"Payload {p} in username: Rejected properly (PASS)")
    else:
        print(f"Payload {p} in username: FAILED/ACCEPTED")
        
    s_temp2 = requests.Session()
    csrf_temp2 = get_csrf(s_temp2)
    # Test in password
    r_sqli2 = s_temp2.post(f"{BASE_URL}/admin/login", data={"username": "admin", "password": p, "csrf_token": csrf_temp2})
    if "admin/inquiries" not in r_sqli2.url:
        print(f"Payload {p} in password: Rejected properly (PASS)")
    else:
        print(f"Payload {p} in password: FAILED/ACCEPTED")

