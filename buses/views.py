from django.shortcuts import render
from django.db.models import Q
from .models import Route, Schedule
from datetime import datetime

def home(request):
    popular_routes = Route.objects.filter(is_active=True)[:6]
    return render(request, 'buses/home.html', {'popular_routes': popular_routes})

def search(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    travel_date = request.GET.get('travel_date')
    
    schedules = []
    if source and destination and travel_date:
        try:
            date_obj = datetime.strptime(travel_date, '%Y-%m-%d').date()
            schedules = Schedule.objects.filter(
                route__source__icontains=source,
                route__destination__icontains=destination,
                travel_date=date_obj,
                is_active=True,
                available_seats__gt=0
            )
        except ValueError:
            pass # Invalid date format

    context = {
        'schedules': schedules,
        'source': source,
        'destination': destination,
        'travel_date': travel_date
    }
    return render(request, 'buses/search.html', context)

def about(request):
    return render(request, 'buses/about.html')

def contact(request):
    return render(request, 'buses/contact.html')
