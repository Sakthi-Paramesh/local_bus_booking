from django.urls import path
from . import views

urlpatterns = [
    path('select-seat/<int:schedule_id>/', views.select_seat, name='select_seat'),
    path('confirm/', views.confirm_booking, name='confirm_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('ticket/<int:ticket_id>/', views.ticket_view, name='ticket_view'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
