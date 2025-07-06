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

def terms(request):
    return render(request, 'terms.html')

def about(request):
    return render(request, 'about.html')

def base(request):
    unread_count = 0
    if request.user.is_superuser:
        unread_count = PrivateChat.objects.filter(receiver=request.user, sender__is_staff=False).count()
    return render(request, 'base.html', {'unread_count': unread_count})

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



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import PrivateChat
from django.contrib.messages import get_messages  # Ensure PrivateChat model exists


# USER TO ADMIN CHAT
@login_required
def user_chat(request):
    # Clear all previous messages (login success, errors, etc.)
    storage = get_messages(request)
    list(storage)  # Iterate through messages to clear them

    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        messages.error(request, "Admin not available at the moment.")
        return redirect('home')

    messages_qs = PrivateChat.objects.filter(
        Q(sender=request.user, receiver=admin_user) |
        Q(sender=admin_user, receiver=request.user)
    ).order_by('timestamp')

    PrivateChat.objects.filter(sender=admin_user, receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            PrivateChat.objects.create(
                sender=request.user,
                receiver=admin_user,
                message=message_text
            )
        return redirect('user_chat')

    return render(request, 'chat/user_chat.html', {
        'messages': messages_qs,
        'admin_user': admin_user
    })




# ADMIN PANEL TO CHAT WITH USERS
from django.contrib.messages import get_messages  # ✅ Required import
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import PrivateChat

@login_required
@user_passes_test(lambda u: u.is_staff)
def chat_admin(request):
    storage = get_messages(request)
    list(storage)  # Clear all queued messages

    PrivateChat.objects.filter(receiver=request.user, is_read=False).update(is_read=True)

    users = User.objects.exclude(id=request.user.id)
    selected_user = None
    messages_qs = []

    selected_user_id = request.GET.get('user')

    if selected_user_id:
        try:
            selected_user = User.objects.get(id=selected_user_id)
            messages_qs = PrivateChat.objects.filter(
                Q(sender=request.user, receiver=selected_user) |
                Q(sender=selected_user, receiver=request.user)
            ).order_by('timestamp')

            PrivateChat.objects.filter(sender=selected_user, receiver=request.user, is_read=False).update(is_read=True)

            if request.method == 'POST':
                message_text = request.POST.get('message')
                if message_text:
                    PrivateChat.objects.create(
                        sender=request.user,
                        receiver=selected_user,
                        message=message_text
                    )
                return redirect(f'/chat_admin/?user={selected_user.id}')

        except User.DoesNotExist:
            selected_user = None

    return render(request, 'chat/chat_admin.html', {
        'users': users,
        'messages': messages_qs,
        'selected_user': selected_user
    })


# OPTIONAL - UNAUTHORIZED VIEW
def unauthorized(request):
    return render(request, 'chat/unauthorized.html')


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PrivateChat
from django.contrib.auth.models import User

@login_required
def unread_message_count(request):
    # Count unread messages for the logged-in user
    unread_count = PrivateChat.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    return JsonResponse({'unread_count': unread_count})