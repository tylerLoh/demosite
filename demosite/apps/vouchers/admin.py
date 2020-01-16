"""Django admin panel for Item and Price model

For more information please visit
https://docs.djangoproject.com/en/2.2/ref/contrib/admin/
"""

from django.contrib import admin
from .models import Voucher, Redeem


class VoucherAdmin(admin.ModelAdmin):
    # override list_display with sku name and item_type attributes
    list_display = ['code', 'discount_type', 'discount_value']

# Register to admin site
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(Redeem)
