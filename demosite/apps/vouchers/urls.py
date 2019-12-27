from django.urls import path
from . import views

app_name = 'voucher'
urlpatterns = [
    # register verify voucher view
    path(
        'verify_voucher/',
        views.VerifyVoucher.as_view(),
        name="verify_voucher"),
]
