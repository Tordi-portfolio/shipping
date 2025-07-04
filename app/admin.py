
from django.contrib import admin
from .models import ContactMessage

# admin.site.register('Shipment')
# admin.site.register('ContactMessage')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)

from django.contrib import admin
from .models import Shipment

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'full_name', 'email', 'service', 'commodity', 'destination_country', 'status', 'created_at')
    list_filter = ('service', 'commodity', 'status', 'created_at')
    search_fields = ('tracking_id', 'full_name', 'email', 'destination_country')
    readonly_fields = ('tracking_id', 'created_at')
