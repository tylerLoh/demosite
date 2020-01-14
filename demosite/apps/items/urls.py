"""Module urls path

For more information please visit
https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""

from django.urls import path
from . import views

# app_name for url dispatcher
app_name = 'item'

# register voucher view
urlpatterns = [
    path('<slug:sku>', views.ItemView.as_view(), name="purchase"),
]
