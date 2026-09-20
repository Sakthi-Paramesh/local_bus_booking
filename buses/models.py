from django.db import models
from django.core.validators import MinValueValidator

class Bus(models.Model):
    BUS_TYPES = (
        ('Ordinary', 'Ordinary'),
        ('Express', 'Express'),
        ('Deluxe', 'Deluxe'),
        ('AC', 'AC'),
    )
    bus_number = models.CharField(max_length=20, unique=True)
    bus_name = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=20, choices=BUS_TYPES, default='Ordinary')
    total_seats = models.PositiveIntegerField(default=40)
    registration_number = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus_number} - {self.bus_name} ({self.bus_type})"
    
    class Meta:
        verbose_name_plural = "Buses"

class Route(models.Model):
    route_name = models.CharField(max_length=100, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=6, decimal_places=2, help_text="Distance in km")
    estimated_duration = models.DurationField(help_text="Format: HH:MM:SS")
    base_fare = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.route_name

class BusStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=100)
    stop_order = models.PositiveIntegerField()
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['route', 'stop_order']
        unique_together = ('route', 'stop_order')

    def __str__(self):
        return f"{self.route.route_name} - {self.stop_name}"

class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='schedules')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    travel_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    available_seats = models.PositiveIntegerField()
    fare = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['travel_date', 'departure_time']
        unique_together = ('bus', 'travel_date', 'departure_time')

    def __str__(self):
        return f"{self.route.source} to {self.route.destination} on {self.travel_date} ({self.bus.bus_number})"
