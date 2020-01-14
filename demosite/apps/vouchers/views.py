"""Voucher views

for more information about views please check
https://docs.djangoproject.com/en/3.0/topics/http/views/
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from django.core import serializers
from vouchers.models import Voucher


class VerifyVoucher(View):
    """Class to verify voucher code for particular item

    To postback json value for XML HttpRequest
    """

    @staticmethod
    def post(request):
        code = request.POST.get("code")
        item_type = request.POST.get("itemType")

        voucher = Voucher.verify_is_voucher(code)
        if voucher:
            if voucher.verify_eligible_type(item_type):
                if voucher.verify_max_redeem():
                    return JsonResponse({
                        'error': None,
                        'voucher': serializers.serialize('json', [voucher]),
                    })
                else:
                    return JsonResponse({
                        'error': 'Voucher code has been fully redeemed',
                    })
            else:
                return JsonResponse({
                    'error': 'Voucher do not apply to this item',
                })
        else:
            return JsonResponse({
                'error': 'Voucher code doesnt exist',
            })
