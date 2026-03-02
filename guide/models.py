from django.db import models


class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    region = models.CharField(max_length=5)
    results_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query} ({self.type}) - {self.region}"