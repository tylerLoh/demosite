"""Django admin panel for Item and Price model

For more information please visit
https://docs.djangoproject.com/en/2.2/ref/contrib/admin/
"""

from django.contrib import admin
from .models import Item, Price
from django.utils import timezone


class ItemAdmin(admin.ModelAdmin):
    # override list_display with sku name and item_type attributes
    list_display = ['sku', 'name', 'item_type', 'status', 'is_expired']

    def is_expired(self, obj):
        return obj.active_timestamp < timezone.now() < obj.expiry_timestamp

    is_expired.short_description = 'Expired'
    is_expired.boolean = True


# Register to admin site
admin.site.register(Item, ItemAdmin)
admin.site.register(Price)
