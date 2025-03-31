const ctx = document.getElementById('usageChart').getContext('2d');
const usageChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['CPU Usage', 'Memory Usage', 'Storage Usage'],
        datasets: [{
            label: 'System Usage',
            data: [0, 0, 0], // Initial data
            backgroundColor: ['#007bff', '#28a745', '#ffc107'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true, // Enable responsiveness
        maintainAspectRatio: false // Allow custom aspect ratio
    }
});

const updateElement = (id, text) => {
    const element = document.getElementById(id);
    if (element) {
        element.innerText = text;
    }
};

const updateDashboard = async () => {
    try {
        const response = await fetch('/metrics'); // Fetch data from the backend
        const data = await response.json(); // Parse the JSON response

        // Update CPU usage
        updateElement('cpu-usage', `CPU Usage: ${data.cpu.usage}%`);
        updateElement('cpu-cores', `Cores: ${data.cpu.cores}`);
        updateElement('cpu-freq', `Frequency: ${data.cpu.freq} MHz`);

        // Update Memory (RAM) usage
        updateElement('ram-usage', `Memory Usage: ${data.memory.percent}%`);
        
        updateElement('memory-total', `Total: ${data.memory.total} GB`);
        updateElement('memory-used', `Used: ${data.memory.used} GB`);

        // Update Storage usage
        updateElement('storage-usage', `Storage Usage: ${data.disk.percent}%`);
        updateElement('disk-total', `Total: ${data.disk.total} GB`);
        updateElement('disk-used', `Used: ${data.disk.used} GB`);

        // Update chart data
        usageChart.data.datasets[0].data = [
            data.cpu.usage,
            data.memory.percent,
            data.disk.percent
        ];
        usageChart.update();
    } catch (error) {
        console.error('Error fetching metrics:', error); // Log any errors
    }
};

// Refresh the dashboard every 5 seconds
setInterval(updateDashboard, 5000);
document.addEventListener('DOMContentLoaded', updateDashboard);

const updateHyperVInfo = async () => {
    try {
        const response = await fetch('/hyperv'); // Fetch data from the backend
        const data = await response.json(); // Parse the JSON response

        const tableBody = document.getElementById('hyperv-table');
        tableBody.innerHTML = ''; // Clear existing rows

        data.forEach(vm => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${vm.Name}</td>
                <td>${vm.State}</td>
                <td>${vm.CPUUsage}%</td>
                <td>${vm.MemoryAssigned} GB</td>
                <td>${vm.Uptime || 'N/A'}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching Hyper-V info:', error);
    }
};

// Refresh the Hyper-V info every 5 seconds
setInterval(updateHyperVInfo, 5000);
document.addEventListener('DOMContentLoaded', updateHyperVInfo);