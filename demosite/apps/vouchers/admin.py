from django.contrib import admin
from .models import Voucher, Redeem

class VoucherAdmin(admin.ModelAdmin):
	list_display = ['code', 'discount_type', 'discount_value']

admin.site.register(Voucher, VoucherAdmin)
admin.site.register(Redeem)