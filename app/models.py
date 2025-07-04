from django.db import models
from django.contrib.auth.models import User

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at'] # Order by newest first


from django.db import models
from django.contrib.auth.models import User
import uuid

class Shipment(models.Model):
    SERVICE_CHOICES = [
        ('Express', 'Express'),
        ('Standard', 'Standard'),
        ('Economy', 'Economy'),
    ]

    COMMODITY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Documents', 'Documents'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    commodity = models.CharField(max_length=100, choices=COMMODITY_CHOICES)
    destination_country = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Processing', 'Processing'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
    ], default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = self.generate_tracking_id()
        super().save(*args, **kwargs)

    def generate_tracking_id(self):
        return 'TRK-' + str(uuid.uuid4()).split('-')[0].upper()

    def __str__(self):
        return f"{self.tracking_id} - {self.full_name}"
