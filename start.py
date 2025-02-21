import subprocess
import webbrowser
import time
import os
import sys
import signal

# Global process variables
p1 = None
p2 = None

def handle_shutdown(signum, frame):
    print("\nShutting down servers...")
    global p1, p2
    # Terminate the Django backend (p1)
    if p1:
        if os.name == 'nt':
            subprocess.run(f"taskkill /F /T /PID {p1.pid}", shell=True)
        else:
            os.kill(p1.pid, signal.SIGTERM)
    # Terminate the Next.js frontend (p2)
    if p2:
        if os.name == 'nt':
            subprocess.run(f"taskkill /F /T /PID {p2.pid}", shell=True)
        else:
            os.kill(p2.pid, signal.SIGTERM)
    sys.exit(0)

# Set up the shutdown handler for Ctrl+C
signal.signal(signal.SIGINT, handle_shutdown)

try:
    # Determine the correct Python executable from the virtual environment, if it exists.
    python_executable = "python"  # fallback to system python
    if os.path.exists("venv"):
        if os.name == 'nt':
            python_executable = os.path.join("venv", "Scripts", "python.exe")
            python_executable = python_executable.strip().split("\\")[-1]
        else:
            python_executable = os.path.join("venv", "bin", "python")
            python_executable = python_executable.strip().split("/")[-1]

    # Start the Django backend using the appropriate Python executable.
    p1 = subprocess.Popen(f"{python_executable} manage.py runserver", cwd="./backend", shell=True)
    
    # Start the Next.js frontend.
    p2 = subprocess.Popen("npm run start", cwd="./frontend", shell=True)
    
    # Wait a few seconds for the servers to start (you may wish to implement a more robust check).
    time.sleep(5)
    
    # Open the frontend in the default browser.
    webbrowser.open('http://localhost:3000')
    
    print("Servers running... Press Ctrl+C to stop")
    
    # Wait for both processes to finish.
    p1.wait()
    p2.wait()

except Exception as e:
    print(f"Error: {e}")
    handle_shutdown(None, None)
