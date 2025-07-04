
from django.contrib import admin
from .models import ContactMessage

# admin.site.register('Shipment')
# admin.site.register('ContactMessage')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)