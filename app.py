from flask import Flask, render_template, Response, request, redirect, url_for, session, flash
from camera import Camera
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import datetime
import os
import time

app = Flask(__name__)
# Apply ProxyFix to handle X-Forwarded-For headers from ngrok
# x_for=1 means we trust the first proxy (ngrok)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
print("Forensic Readiness: ProxyFix middleware active for IP integrity.")

app.secret_key = 'supersecretkey'  # Hardcoded for simulation

# ensure forensics directory exists
if not os.path.exists('forensics'):
    os.makedirs('forensics')

# Configure Forensics Loggers
def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# Access Logger: Timestamp, Status, Source IP
access_logger = setup_logger('access_logger', 'forensics/access_control.log')
# Stream Logger: Timestamp, Event
stream_logger = setup_logger('stream_logger', 'forensics/stream_events.log')

def log_access(status, ip):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"{timestamp},{status},{ip}"
    access_logger.info(log_entry)

def log_stream_event(event):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"{timestamp},{event}"
    stream_logger.info(log_entry)

@app.route('/index')
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.remote_addr
        
        # Hardcoded credentials
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            log_access('SUCCESS', ip)
            return redirect(url_for('index'))
        else:
            log_access('FAILURE', ip)
            flash('Invalid credentials')
            return render_template('login.html')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def gen(camera):
    log_stream_event('STREAM_STARTED')
    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.04) # Limit FPS roughly to video FPS
    except GeneratorExit:
        log_stream_event('STREAM_INTERRUPTED')
    except Exception as e:
        log_stream_event(f'STREAM_ERROR: {str(e)}')
    finally:
        # This might not always be reached in a generator depending on WSGI server
        pass

@app.route('/video_feed')
def video_feed():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
