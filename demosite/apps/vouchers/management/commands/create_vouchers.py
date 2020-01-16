"""Django command to create sample data for Voucher Model

This command allows user to create sample data for Voucher
    python manage.py create_vouchers [int]
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db import IntegrityError
from vouchers.models import Voucher
from demosite.utils.class_define import ItemType, DiscountType
from datetime import timedelta


class Command(BaseCommand):
    """Command class to inherit Django BaseCommand

    Attributes
    ----------
    help: str
        A message to print out using -h option
    """

    help = "create sample voucher data"

    def handle(self, *args, **kwargs):
        """Create sample data with DiscountType and ItemType

        Eg. 2 Discount Type and 3 Item Type
        N * K, which means each unique item type will have 2 diff voucher type
        """
        current_time = timezone.now()
        for discount in DiscountType:
            count = 1
            for item in ItemType:
                try:
                    voucher = Voucher()
                    voucher.code = item.name[:5] + '0000' + str(count)
                    voucher.discount_type = discount.value
                    voucher.discount_value = (
                        10 if discount.value == '%' else 30)
                    voucher.eligible_type = str(item.value)
                    voucher.copied = 2
                    voucher.active_timestamp = current_time - timedelta(days=10)
                    voucher.expiry_timestamp = current_time + timedelta(days=10)

                    voucher.save()
                    count = count + 1
                except IntegrityError as e:
                    pass
