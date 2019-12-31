from django.urls import path

from . import views

app_name = 'item'
urlpatterns = [
    path('<slug:sku>', views.ItemView.as_view(), name="purchase"),
]
