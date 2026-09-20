from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from buses.models import Bus, Route, BusStop, Schedule
from datetime import datetime, timedelta, time

class Command(BaseCommand):
    help = 'Loads demo data for GovBus application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        Schedule.objects.all().delete()
        BusStop.objects.all().delete()
        Route.objects.all().delete()
        Bus.objects.all().delete()

        self.stdout.write('Loading buses...')
        buses_data = [
            {'number': 'TN-DEMO-101', 'name': 'City Express', 'type': 'Express'},
            {'number': 'TN-DEMO-102', 'name': 'City Express', 'type': 'Express'},
            {'number': 'TN-DEMO-201', 'name': 'Super Deluxe', 'type': 'Deluxe'},
            {'number': 'TN-DEMO-202', 'name': 'Super Deluxe', 'type': 'Deluxe'},
            {'number': 'TN-DEMO-301', 'name': 'AC Sleeper', 'type': 'AC'},
            {'number': 'TN-DEMO-401', 'name': 'Ordinary Town Bus', 'type': 'Ordinary'},
            {'number': 'TN-DEMO-402', 'name': 'Ordinary Town Bus', 'type': 'Ordinary'},
            {'number': 'TN-DEMO-501', 'name': 'Intercity AC', 'type': 'AC'},
        ]
        buses = []
        for bd in buses_data:
            bus = Bus.objects.create(
                bus_number=bd['number'],
                bus_name=bd['name'],
                bus_type=bd['type'],
                total_seats=40,
                registration_number=f"REG-{bd['number']}"
            )
            buses.append(bus)

        self.stdout.write('Loading routes...')
        routes_data = [
            {'name': 'Chennai-Tambaram', 'src': 'Chennai', 'dest': 'Tambaram', 'dist': 30, 'dur': '01:15:00', 'fare': 35},
            {'name': 'Chennai-Avadi', 'src': 'Chennai', 'dest': 'Avadi', 'dist': 25, 'dur': '01:00:00', 'fare': 30},
            {'name': 'Chennai-Chengalpattu', 'src': 'Chennai', 'dest': 'Chengalpattu', 'dist': 60, 'dur': '01:45:00', 'fare': 65},
            {'name': 'Coimbatore-Tiruppur', 'src': 'Coimbatore', 'dest': 'Tiruppur', 'dist': 55, 'dur': '01:30:00', 'fare': 60},
            {'name': 'Coimbatore-Mettupalayam', 'src': 'Coimbatore', 'dest': 'Mettupalayam', 'dist': 40, 'dur': '01:10:00', 'fare': 45},
            {'name': 'Erode-Salem', 'src': 'Erode', 'dest': 'Salem', 'dist': 65, 'dur': '01:40:00', 'fare': 70},
            {'name': 'Madurai-Dindigul', 'src': 'Madurai', 'dest': 'Dindigul', 'dist': 65, 'dur': '01:30:00', 'fare': 75},
            {'name': 'Trichy-Thanjavur', 'src': 'Trichy', 'dest': 'Thanjavur', 'dist': 60, 'dur': '01:20:00', 'fare': 65},
        ]
        routes = []
        for rd in routes_data:
            route = Route.objects.create(
                route_name=rd['name'],
                source=rd['src'],
                destination=rd['dest'],
                distance=rd['dist'],
                estimated_duration=timedelta(hours=int(rd['dur'].split(':')[0]), minutes=int(rd['dur'].split(':')[1])),
                base_fare=rd['fare']
            )
            routes.append(route)
            
            # Create dummy stops
            BusStop.objects.create(route=route, stop_name=f"{rd['src']} Main Bus Stand", stop_order=1)
            BusStop.objects.create(route=route, stop_name=f"Middle Point", stop_order=2)
            BusStop.objects.create(route=route, stop_name=f"{rd['dest']} Terminus", stop_order=3)

        self.stdout.write('Loading schedules...')
        # Create schedules for next 7 days
        today = datetime.now().date()
        for i in range(7):
            travel_date = today + timedelta(days=i)
            # Add schedules for each route
            for j, route in enumerate(routes):
                # Pick a bus based on index
                bus = buses[j % len(buses)]
                
                # Morning schedule
                Schedule.objects.create(
                    bus=bus,
                    route=route,
                    travel_date=travel_date,
                    departure_time=time(8, 30),
                    arrival_time=time(10, 0),  # Rough approximation
                    available_seats=bus.total_seats,
                    fare=route.base_fare
                )
                
                # Evening schedule
                Schedule.objects.create(
                    bus=buses[(j+1) % len(buses)],
                    route=route,
                    travel_date=travel_date,
                    departure_time=time(17, 15),
                    arrival_time=time(19, 0),
                    available_seats=bus.total_seats,
                    fare=route.base_fare
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded demo data!'))
