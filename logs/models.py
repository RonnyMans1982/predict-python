from django.db import models

from logs.file_service import get_logs


class Log(models.Model):
    """A XES log file on disk"""
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)

    def get_file(self):
        """Read and parse log from filesystem"""
        return get_logs(self.path)