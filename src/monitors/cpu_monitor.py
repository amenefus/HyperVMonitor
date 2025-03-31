import psutil

class CPUMonitor:
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_cpu_stats(self):
        return psutil.cpu_stats()