"""Module urls path

For more information please visit
https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""

from django.urls import path
from . import views

# app_name for url dispatcher
app_name = "voucher"

# register voucher view
urlpatterns = [
    path(
        'verify_voucher/',
        views.VerifyVoucher.as_view(),
        name="verify_voucher"),
]
