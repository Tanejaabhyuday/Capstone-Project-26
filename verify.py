import requests
import time
import sys

BASE_URL = "http://localhost:5001"
LOGIN_URL = f"{BASE_URL}/login"
INDEX_URL = f"{BASE_URL}/index"
FEED_URL = f"{BASE_URL}/video_feed"

def test_access_denied():
    print("Testing Access Denied...", end=" ")
    r = requests.get(INDEX_URL, allow_redirects=False)
    if r.status_code == 302 and "login" in r.headers['Location']:
        print("PASS")
    else:
        print(f"FAIL (Status: {r.status_code}, Location: {r.headers.get('Location')})")

def test_login_failure():
    print("Testing Login Failure...", end=" ")
    data = {'username': 'admin', 'password': 'wrongpassword'}
    r = requests.post(LOGIN_URL, data=data)
    if "Invalid credentials" in r.text or "Security Camera Access" in r.text:
        print("PASS")
    else:
        print("FAIL")

def test_login_success():
    print("Testing Login Success...", end=" ")
    data = {'username': 'admin', 'password': 'admin'}
    s = requests.Session()
    r = s.post(LOGIN_URL, data=data) 
    if r.status_code == 200 and "Live Camera Feed" in r.text:
        print("PASS")
        return s
    else:
        print(f"FAIL (Status: {r.status_code})")
        return None

def test_stream_access(session):
    print("Testing Video Stream Access...", end=" ")
    r = session.get(FEED_URL, stream=True)
    if r.status_code == 200 and "multipart/x-mixed-replace" in r.headers['Content-Type']:
        print("PASS")
        r.close()
    else:
        print(f"FAIL (Status: {r.status_code}, Content-Type: {r.headers.get('Content-Type')})")

def verify_logs():
    print("\nVerifying Logs...")
    
    # Check Access Log
    try:
        with open('forensics/access_control.log', 'r') as f:
            logs = f.read()
            if "SUCCESS" in logs and "FAILURE" in logs:
                print("  Access Control Log: PASS (Found SUCCESS and FAILURE entries)")
            else:
                print(f"  Access Control Log: FAIL (Content: {logs})")
    except FileNotFoundError:
        print("  Access Control Log: FAIL (File not found)")

    # Check Stream Log
    try:
        with open('forensics/stream_events.log', 'r') as f:
            logs = f.read()
            if "STREAM_STARTED" in logs:
                print("  Stream Events Log: PASS (Found STREAM_STARTED)")
            else:
                print(f"  Stream Events Log: FAIL (Content: {logs})")
    except FileNotFoundError:
        print("  Stream Events Log: FAIL (File not found)")

if __name__ == "__main__":
    # Ensure server is up
    try:
        requests.get(LOGIN_URL)
    except requests.exceptions.ConnectionError:
        print("Error: Server not running on localhost:5000")
        sys.exit(1)

    test_access_denied()
    test_login_failure()
    session = test_login_success()
    if session:
        test_stream_access(session)
    
    # Wait a moment for logs to flush
    time.sleep(1)
    verify_logs()
