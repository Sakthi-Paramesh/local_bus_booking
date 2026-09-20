from django.contrib import admin
from .models import Bus, Route, BusStop, Schedule

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'bus_name', 'bus_type', 'total_seats', 'is_active')
    list_filter = ('bus_type', 'is_active')
    search_fields = ('bus_number', 'bus_name')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'source', 'destination', 'base_fare', 'is_active')
    search_fields = ('route_name', 'source', 'destination')
    list_filter = ('is_active',)

@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ('route', 'stop_name', 'stop_order', 'arrival_time', 'departure_time')
    search_fields = ('stop_name', 'route__route_name')
    list_filter = ('route',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus', 'route', 'travel_date', 'departure_time', 'available_seats', 'fare', 'is_active')
    list_filter = ('travel_date', 'is_active', 'route')
    search_fields = ('bus__bus_number', 'route__route_name')
