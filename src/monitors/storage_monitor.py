import psutil

class StorageMonitor:
    def __init__(self):
        self.storage_info = self.get_storage_info()

    def get_storage_info(self):
        disk_usage = psutil.disk_usage('/')
        return {
            'total': disk_usage.total,
            'used': disk_usage.used,
            'free': disk_usage.free,
            'percent': disk_usage.percent
        }

    def get_metrics(self):
        return self.storage_info