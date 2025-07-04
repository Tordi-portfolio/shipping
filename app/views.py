from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import ContactForm
from .models import ContactMessage

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')  # Change to your actual home view name
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def home(request):
    return render(request, 'home.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_success') # Redirect to a success page or back to contact
        else:
            messages.error(request, 'There was an error with your submission. Please check the form.')
    else:
        form = ContactForm()
    return render(request, 'message/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'message/contact_success.html') # Create a simple success page

# Test function to check if user is staff (admin)
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def receive_messages(request):
    messages = ContactMessage.objects.all()
    return render(request, 'message/receive_messages.html', {'messages': messages})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Shipment
from .forms import ShipmentForm

@login_required
def create_shipment(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.user = request.user
            shipment.save()
            return render(request, 'tracking/shipment_success.html', {
                'tracking_id': shipment.tracking_id,
                'message': 'Shipment created successfully!'
            })
    else:
        form = ShipmentForm()
    return render(request, 'tracking/create_shipment.html', {'form': form})


def track_shipment(request):
    if request.method == 'POST':
        tracking_id = request.POST['tracking_id']
        try:
            shipment = Shipment.objects.get(tracking_id=tracking_id)
            return render(request, 'tracking/tracking_result.html', {'shipment': shipment})
        except Shipment.DoesNotExist:
            return render(request, 'tracking/tracking_result.html', {'error': 'Tracking ID not found'})
    return render(request, 'tracking/track_shipment.html')
