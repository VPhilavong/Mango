import subprocess
import webbrowser
import time
import os
import sys
from signal import signal, SIGINT

def handle_shutdown(signum, frame):
    print("\nShutting down servers...")
    # Kill processes on Windows
    subprocess.run("taskkill /F /T /PID %i" % p1.pid, shell=True)
    subprocess.run("taskkill /F /T /PID %i" % p2.pid, shell=True)
    sys.exit(0)

# Set up shutdown handler
signal(SIGINT, handle_shutdown)

try:
    # Activate virtual environment if exists
    if os.path.exists("venv"):
        activate_script = os.path.join("venv", "Scripts", "activate")
        subprocess.run(f"call {activate_script}", shell=True)

    # Run Django Backend
    p1 = subprocess.Popen("python manage.py runserver", cwd="./backend", shell=True)
    
    # Run Next Frontend
    #subprocess.run("npm run build", cwd='./frontend', shell=True)  # Build
    p2 = subprocess.Popen("npm run start", cwd='./frontend', shell=True)
    
    # Wait for servers to start
    time.sleep(5)
    
    # Open browser
    webbrowser.open('http://localhost:3000')
    
    print("Servers running... Press Ctrl+C to stop")
    p1.wait()
    p2.wait()

except Exception as e:
    print(f"Error: {e}")
    handle_shutdown(None, None)