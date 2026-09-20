from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PassengerProfileForm
from .models import PassengerProfile
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = PassengerProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = PassengerProfileForm()
        
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except PassengerProfile.DoesNotExist:
        profile = PassengerProfile(user=request.user)

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        # Remove password validation for profile update if they are just updating info
        if 'password' not in request.POST or not request.POST['password']:
            user_form.fields['password'].required = False
            user_form.fields['password_confirm'].required = False
            
        profile_form = PassengerProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data.get('password'):
                user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        # Pre-populate without password
        user_form = UserRegistrationForm(instance=request.user)
        user_form.fields['password'].required = False
        user_form.fields['password_confirm'].required = False
        profile_form = PassengerProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def dashboard(request):
    bookings = request.user.bookings.all()
    context = {
        'total_bookings': bookings.count(),
        'completed_trips': bookings.filter(status='COMPLETED').count(),
        'cancelled_trips': bookings.filter(status='CANCELLED').count(),
        'upcoming_trips': bookings.filter(status='CONFIRMED').count(),
        'recent_bookings': bookings[:5]
    }
    return render(request, 'accounts/dashboard.html', context)
