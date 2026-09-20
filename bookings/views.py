from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from buses.models import Schedule
from .models import Booking, Ticket
import qrcode
from io import BytesIO
from django.core.files import File
from datetime import datetime

@login_required
def select_seat(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    # Get all booked seats for this schedule
    booked_seats = Booking.objects.filter(
        schedule=schedule, 
        status__in=['CONFIRMED', 'COMPLETED']
    ).values_list('seat_number', flat=True)

    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        if not seat_number:
            messages.error(request, 'Please select a seat.')
            return redirect('select_seat', schedule_id=schedule_id)
        
        seat_number = int(seat_number)
        if seat_number in booked_seats:
            messages.error(request, 'This seat is already booked.')
            return redirect('select_seat', schedule_id=schedule_id)

        # Proceed to confirmation page
        request.session['booking_data'] = {
            'schedule_id': schedule.id,
            'seat_number': seat_number
        }
        return redirect('confirm_booking')

    # Standard bus has e.g. 40 seats. Pass a range to the template
    total_seats = schedule.bus.total_seats
    seats_list = list(range(1, total_seats + 1))
    
    context = {
        'schedule': schedule,
        'seats': seats_list,
        'booked_seats': list(booked_seats),
    }
    return render(request, 'bookings/select_seat.html', context)

@login_required
def confirm_booking(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        messages.error(request, 'No active booking session.')
        return redirect('home')

    schedule = get_object_or_404(Schedule, id=booking_data['schedule_id'])
    seat_number = booking_data['seat_number']

    if request.method == 'POST':
        passenger_name = request.POST.get('passenger_name')
        passenger_phone = request.POST.get('passenger_phone')

        if not passenger_name or not passenger_phone:
            messages.error(request, 'Please provide passenger details.')
            return redirect('confirm_booking')

        # Check availability again
        if Booking.objects.filter(schedule=schedule, seat_number=seat_number, status__in=['CONFIRMED', 'COMPLETED']).exists():
            messages.error(request, 'Sorry, this seat was just booked by someone else.')
            return redirect('select_seat', schedule_id=schedule.id)

        # Create Booking
        booking = Booking.objects.create(
            user=request.user,
            schedule=schedule,
            seat_number=seat_number,
            passenger_name=passenger_name,
            passenger_phone=passenger_phone,
            travel_date=schedule.travel_date,
            amount=schedule.fare,
            status='CONFIRMED'
        )

        # Update available seats
        schedule.available_seats -= 1
        schedule.save()

        # Generate Ticket & QR
        ticket = Ticket.objects.create(booking=booking)
        
        qr_data = f"Ticket: {ticket.ticket_number} | Booking: {booking.booking_id} | Name: {booking.passenger_name} | Bus: {schedule.bus.bus_number} | Route: {schedule.route.route_name} | Date: {schedule.travel_date} | Seat: {seat_number} | Status: CONFIRMED"
        qr = qrcode.make(qr_data)
        
        blob = BytesIO()
        qr.save(blob, 'JPEG')
        ticket.qr_code.save(f'qr_{ticket.ticket_number}.jpg', File(blob), save=True)

        del request.session['booking_data']
        messages.success(request, 'Booking Confirmed Successfully!')
        return redirect('ticket_view', ticket_id=ticket.id)

    context = {
        'schedule': schedule,
        'seat_number': seat_number,
    }
    return render(request, 'bookings/confirm_booking.html', context)

@login_required
def my_bookings(request):
    bookings = request.user.bookings.all().order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, booking__user=request.user)
    return render(request, 'bookings/ticket.html', {'ticket': ticket})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        # Check if they can cancel (e.g. before travel date/time)
        current_date = datetime.now().date()
        if booking.travel_date < current_date:
            messages.error(request, 'Cannot cancel past bookings.')
        elif booking.status == 'CANCELLED':
            messages.error(request, 'Booking is already cancelled.')
        else:
            booking.status = 'CANCELLED'
            booking.save()
            
            # Increase available seats
            booking.schedule.available_seats += 1
            booking.schedule.save()
            
            messages.success(request, 'Booking cancelled successfully.')
            
    return redirect('my_bookings')
