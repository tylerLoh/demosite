from django.contrib import admin
from .models import Item, Price

class ItemAdmin(admin.ModelAdmin):
	list_display = ['sku', 'name', 'item_type']

admin.site.register(Item, ItemAdmin)
admin.site.register(Price)
