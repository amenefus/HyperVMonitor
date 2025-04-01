# System Monitor

This project is a modern Windows application that monitors system metrics such as CPU usage, RAM, storage, and Hyper-V virtual machine information. It features a dynamic dashboard that refreshes every 5 seconds.

## Features

- Real-time monitoring of:
  - **CPU Usage**
  - **RAM Usage**
  - **Storage Usage**
- Integration with **Hyper-V** to display virtual machine details:
  - VM Name
  - State (Running, Off, etc.)
  - CPU Usage
  - Memory Assigned
  - Uptime
- Dynamic dashboard built with Flask, JavaScript, and Bootstrap.

---

## Project Structure

```
system-monitor
├── src
│   ├── app.py                # Entry point of the application
│   ├── monitors              # Package containing monitoring classes
│   │   ├── __init__.py
│   │   ├── cpu_monitor.py     # Class for CPU monitoring
│   │   ├── memory_monitor.py  # Class for RAM monitoring
│   │   └── storage_monitor.py # Class for storage monitoring
│   ├── static                # Static files for the dashboard
│   │   ├── css
│   │   │   └── styles.css     # CSS styles for the dashboard
│   │   └── js
│   │       └── dashboard.js   # JavaScript for dynamic updates
│   └── templates             # HTML templates for the dashboard
│       ├── base.html         # Base template
│       └── index.html        # Dashboard view
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## Setup Instructions

### Prerequisites
- **Python 3.8+** installed on your system.
- **Windows OS** with **Hyper-V** enabled and configured.
- Administrative privileges to run the application.

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd system-monitor
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python src/app.py
   ```

4. **Access the dashboard**:
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

---

## Usage

### Dashboard Features
- **System Metrics**:
  - Displays real-time CPU, RAM, and storage usage.
  - Automatically refreshes every 5 seconds.
- **Hyper-V Virtual Machines**:
  - Lists all virtual machines on the host.
  - Displays VM name, state, CPU usage, memory assigned, and uptime.

### Hyper-V Integration
The application uses PowerShell cmdlets to fetch Hyper-V virtual machine information. The following PowerShell command is executed internally:
```powershell
Get-VM | Select-Object Name, State, @{Name='CPUUsage';Expression={(Get-VMProcessor -VMName $_.Name).LoadPercentage}}, 
@{Name='MemoryAssigned';Expression={$_.MemoryAssigned / 1GB}}, Uptime | ConvertTo-Json -Depth 2
```

---

## Example Output

### System Metrics
The dashboard displays the following system metrics:
- **CPU Usage**: Percentage of CPU utilization.
- **RAM Usage**: Total, used, and percentage of memory usage.
- **Storage Usage**: Total, used, and percentage of disk usage.

### Hyper-V Virtual Machines
The `/hyperv` endpoint returns JSON data like this:
```json
[
    {
        "Name": "VM1",
        "State": "Running",
        "CPUUsage": 10,
        "MemoryAssigned": 4.0,
        "Uptime": "1:23:45"
    },
    {
        "Name": "VM2",
        "State": "Off",
        "CPUUsage": 0,
        "MemoryAssigned": 0.0,
        "Uptime": null
    }
]
```

The dashboard displays this data in a table format.

---

## Troubleshooting

### Common Issues
1. **PowerShell Errors**:
   - Ensure that PowerShell is installed and accessible.
   - Verify that the execution policy allows running scripts:
     ```powershell
     Get-ExecutionPolicy
     ```
     If needed, set the execution policy to `RemoteSigned`:
     ```powershell
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

2. **Administrative Privileges**:
   - The application requires administrative privileges to access Hyper-V data. Run the Flask app as an administrator:
     ```bash
     python src/app.py
     ```

3. **Hyper-V Not Enabled**:
   - Ensure that Hyper-V is enabled on your Windows machine. You can enable it via the "Turn Windows features on or off" menu.

4. **Empty Hyper-V Data**:
   - If the `/hyperv` endpoint returns an empty response, ensure that there are virtual machines configured in Hyper-V Manager.

---

## Dependencies

The project uses the following Python libraries:
- **Flask**: Web framework for building the dashboard.
- **Flask-Cors**: Enables Cross-Origin Resource Sharing (CORS) for API endpoints.
- **psutil**: Fetches system metrics like CPU, memory, and disk usage.
- **pywin32**: Provides access to Windows APIs, including WMI for Hyper-V integration.

Install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.
