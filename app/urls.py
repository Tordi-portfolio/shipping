from django.urls import path
from . import views
from .views import unread_message_count 

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('contact', views.contact, name='contact'),
    path('contact_success', views.contact_success, name='contact_success'),
    path('receive_messages', views.receive_messages, name='receive_messages'),

    path('create_shipment', views.create_shipment, name='create_shipment'),
    path('track_shipment', views.track_shipment, name='track_shipment'),

    path('about', views.about, name='about'),
    path('terms', views.terms, name='terms'),
    path('user_chat', views.user_chat, name='user_chat'),
    path('chat_admin/', views.chat_admin, name='chat_admin'),

    path('base', views.base, name='base'),
    # path('ajax/unread-count/', unread_message_count, name='unread_message_count'),
    path('unread-message-count/', views.unread_message_count, name='unread_message_count'),

]
