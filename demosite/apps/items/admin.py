"""Django admin panel for Item and Price model

For more information please visit
https://docs.djangoproject.com/en/2.2/ref/contrib/admin/
"""

from django.contrib import admin
from .models import Item, Price


class ItemAdmin(admin.ModelAdmin):
    # override list_display with sku name and item_type attributes
    list_display = ['sku', 'name', 'item_type']


# Register to admin site
admin.site.register(Item, ItemAdmin)
admin.site.register(Price)
