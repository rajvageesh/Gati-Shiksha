import requests

BASE_URL = 'http://127.0.0.1:8000'

def get_csrf(session):
    r = session.get(BASE_URL + '/')
    for line in r.text.split('\n'):
        if 'name="csrf_token"' in line:
            return line.split('value="')[1].split('"')[0]
    return ''

s = requests.Session()

print("=== EMAIL SECURITY TESTS ===")

def test_email(email_str, desc, expect_reject=True):
    s_temp = requests.Session()
    csrf = get_csrf(s_temp)
    data = {
        'csrf_token': csrf,
        'name': 'Test User',
        'email': email_str,
        'role': 'Student',
        'message': 'Testing email validation',
        'program': ''
    }
    r = s_temp.post(f"{BASE_URL}/submit-inquiry", data=data)
    
    if expect_reject:
        if "Invalid email address" in r.text or "Please enter a valid email address" in r.text or "Input exceeds allowed length" in r.text or "fill in all required fields" in r.text or "Too many requests" in r.text or "already submitted recently" in r.text:
            print(f"[{desc}] '{email_str}' -> REJECTED (PASS)")
        else:
            print(f"[{desc}] '{email_str}' -> ACCEPTED (FAIL - Should have rejected)")
    else:
        # Expected to accept, which might mean "success" flash or "Too many requests" if rate limited,
        # but NOT "valid email address" error.
        if "Please enter a valid email address" not in r.text and "Input exceeds allowed length" not in r.text:
            print(f"[{desc}] '{email_str}' -> ACCEPTED (PASS)")
        else:
            print(f"[{desc}] '{email_str}' -> REJECTED (FAIL - Should have accepted)")

# Normal emails
test_email("user@gmail.com", "Gmail address", False)
test_email("user@outlook.com", "Outlook address", False)
test_email("student@university.edu", "Normal custom domain", False)

# Invalid emails
test_email("abc", "Missing domain")
test_email("abc@", "Missing TLD")
test_email("@example.com", "Missing local part")
test_email("abc@.com", "Invalid domain format")
test_email("abc..test@example.com", "Consecutive dots")

# Security payloads
test_email("A" * 260 + "@example.com", "Oversized email")
test_email("test@example.com\r\nCC: victim@example.com", "CR/LF injection")
test_email("test@example.com\nBCC: victim@example.com", "LF injection")
test_email("<script>alert(1)</script>@example.com", "XSS in email")

