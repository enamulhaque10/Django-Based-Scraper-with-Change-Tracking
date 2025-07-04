from django.db import models

class ScrapedItem(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField(blank=True)
    description = models.TextField()
    reference_date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class ChangeLog(models.Model):
    CHANGE_TYPE = (
        ('added', 'Added'),
        ('removed', 'Removed'),
    )
    title = models.CharField(max_length=255)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)

