from django.db import models
from django.contrib.auth.models import User
from buses.models import Schedule
import uuid

class Booking(models.Model):
    STATUS_CHOICES = (
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

    booking_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='bookings')
    seat_number = models.PositiveIntegerField()
    passenger_name = models.CharField(max_length=100)
    passenger_phone = models.CharField(max_length=15)
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booking_date']
        # Prevent double booking of the same seat on the same schedule
        unique_together = ('schedule', 'seat_number', 'status')

    def __str__(self):
        return f"{self.booking_id} - {self.passenger_name}"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Generate a unique booking ID (e.g., GB-UUID)
            unique_id = str(uuid.uuid4().hex[:8]).upper()
            self.booking_id = f"GB{unique_id}"
        super().save(*args, **kwargs)

class Ticket(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='ticket')
    ticket_number = models.CharField(max_length=30, unique=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket_number

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{self.booking.booking_id}"
        super().save(*args, **kwargs)
