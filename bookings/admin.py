from django.contrib import admin
from .models import Booking, Ticket

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'passenger_name', 'schedule', 'seat_number', 'travel_date', 'status')
    list_filter = ('status', 'travel_date', 'created_at')
    search_fields = ('booking_id', 'passenger_name', 'passenger_phone')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'booking', 'issued_at')
    search_fields = ('ticket_number', 'booking__booking_id')
