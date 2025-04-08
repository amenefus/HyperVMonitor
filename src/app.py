from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import psutil
import time
from threading import Thread
import platform
from datetime import datetime
import subprocess
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCIDENTS_FILE = os.path.join(BASE_DIR, 'static', 'incidents.csv')

if not os.path.exists(INCIDENTS_FILE):
    with open(INCIDENTS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Hostname', 'Issue', 'Status'])

app = Flask(__name__)
CORS(app)

def get_system_metrics():
    """Get system metrics including CPU, RAM, and storage usage"""
    try:
        print("Fetching CPU usage...")
        cpu_usage = psutil.cpu_percent(interval=0.1)  # Short sampling period
        cpu_cores = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
    except Exception as e:
        print(f"Error fetching CPU metrics: {e}")
        cpu_usage, cpu_cores, cpu_freq = 0, 0, 0

    try:
        print("Fetching memory usage...")
        memory = psutil.virtual_memory()
        memory_total = round(memory.total / (1024.0 ** 3), 2)
        memory_used = round(memory.used / (1024.0 ** 3), 2)
        memory_percent = memory.percent
    except Exception as e:
        print(f"Error fetching memory metrics: {e}")
        memory_total, memory_used, memory_percent = 0, 0, 0

    try:
        print("Fetching disk usage...")
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024.0 ** 3), 2)
        disk_used = round(disk.used / (1024.0 ** 3), 2)
        disk_percent = disk.percent
    except Exception as e:
        print(f"Error fetching disk metrics: {e}")
        disk_total, disk_used, disk_percent = 0, 0, 0

    metrics = {
        'cpu': {
            'usage': cpu_usage,
            'cores': cpu_cores,
            'freq': cpu_freq
        },
        'memory': {
            'total': memory_total,
            'used': memory_used,
            'percent': memory_percent
        },
        'disk': {
            'total': disk_total,
            'used': disk_used,
            'percent': disk_percent
        },
        'system': {
            'os': platform.system(),
            'version': platform.version(),
            'machine': platform.machine(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    #Writing to Incidents file if CPU usage exceeds a threshold
    if cpu_usage > 75:  # Example threshold for CPU usage
        log_incident(cpu_usage)

    print(metrics)  # Debugging: Log the metrics to the console
    return metrics

def get_hyperv_info():
    """Fetch information about Hyper-V virtual machines using PowerShell."""
    try:
        print("Fetching Hyper-V information using PowerShell...")
        # PowerShell command to get VM details
        command = [
            "powershell",
            "-Command",
            "Get-VM | Select-Object Name, State, @{Name='CPUUsage';Expression={(Get-VMProcessor -VMName $_.Name).LoadPercentage}}, "
            "@{Name='MemoryAssigned';Expression={$_.MemoryAssigned / 1GB}}, Uptime | ConvertTo-Json -Depth 2"
        ]
        # Execute the PowerShell command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Parse the JSON output from PowerShell
        vm_info = json.loads(result.stdout)
        return vm_info
    except subprocess.CalledProcessError as e:
        print(f"Error executing PowerShell command: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing PowerShell output: {e}")
        return []

def log_incident(cpu_usage):
    """Log an incident when CPU usage exceeds the threshold."""
    print(f"Logging incident: CPU usage is {cpu_usage}%")  # Debugging
    hostname = platform.node()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    issue_title = f"High CPU Usage: {cpu_usage}%"
    incident = [timestamp, hostname, issue_title, "Pending"]

    # Append the incident to the CSV file
    with open(INCIDENTS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(incident)

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    """API endpoint to get system metrics"""
    print("Metrics endpoint called")  # Debugging: Log when the endpoint is called
    return jsonify(get_system_metrics())

@app.route('/hyperv')
def hyperv():
    """API endpoint to get Hyper-V virtual machine information."""
    return jsonify(get_hyperv_info())

@app.route('/incidents', methods=['GET', 'POST'])
def incidents():
    """API endpoint to handle incidents."""
    if request.method == 'GET':
        # Read incidents from the CSV file
        try:
            with open(INCIDENTS_FILE, 'r') as file:
                reader = csv.reader(file)
                incidents = [row for row in reader]
            return jsonify(incidents)
        except FileNotFoundError:
            return jsonify([])

    elif request.method == 'POST':
        # Mark an incident as acknowledged
        data = request.json
        incident_id = data.get('id')
        updated_incidents = []

        with open(INCIDENTS_FILE, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == incident_id:
                    row[3] = "Acknowledged"
                updated_incidents.append(row)

        with open(INCIDENTS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_incidents)

        return jsonify({"message": "Incident updated successfully"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)