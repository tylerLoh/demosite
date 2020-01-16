"""Unit Test for Voucher, involving some business flow as below:

1)
"""

from django.test import TestCase
from django.db.models import Count
from vouchers.models import Voucher
from demosite.utils.class_define import ItemType, DiscountType
from random import randint
from django.utils import timezone
from datetime import timedelta


class VoucherTestCase(TestCase):

    def setUp(self):
        for discount in DiscountType:
            for item in ItemType:
                voucher = Voucher()
                voucher.code = item.name[:5] + str(randint(10000, 99999))
                voucher.discount_type = discount.value
                voucher.discount_value = (10 if discount.value == '%' else 30)
                voucher.eligible_type = str(item.value)
                voucher.copied = 2
                voucher.active_timestamp = timezone.now()
                voucher.expiry_timestamp = timezone.now() + timedelta(days=10)
                voucher.save()

    def test_valid_voucher_code(self):
        # Test is valid voucher code
        valid_voucher = Voucher.objects.first()
        voucher = Voucher.verify_is_voucher(valid_voucher.code)

        self.assertIsInstance(voucher, Voucher)

    def test_invalid_voucher_code(self):
        # Test fir invalid or non-exist voucher code
        self.assertIsNone(Voucher.verify_is_voucher("#321#"))

    def test_valid_redemption(self):
        """Voucher can be redeem

        1) Redeem datetime must >= voucher active datetime and <= expiry
           datetime.
        2) Total redeemed less than copied count
        """

        current_datetime = timezone.now()
        product_voucher = Voucher.objects.filter(
            eligible_type='1',
            active_timestamp__lte=current_datetime,
            expiry_timestamp__gte=current_datetime).annotate(
            redeem_count=Count('redeem')).filter(redeem_count__gte=0).first()

        treatment_voucher = Voucher.objects.filter(
            eligible_type='2',
            active_timestamp__lte=current_datetime,
            expiry_timestamp__gte=current_datetime).annotate(
            redeem_count=Count('redeem')).filter(redeem_count__gte=0).first()

        # try redeem on product
        self.assertTrue(product_voucher.verify_eligible_type(1))
        self.assertFalse(product_voucher.verify_is_expired())
        self.assertTrue(product_voucher.verify_max_redeem())

        self.assertTrue(treatment_voucher.verify_eligible_type(2))
        self.assertFalse(treatment_voucher.verify_is_expired())
        self.assertTrue(treatment_voucher.verify_max_redeem())

    def test_invalid_redemption(self):
        # test invalid redemption type and over redeem
        current_datetime = timezone.now()

        # get product voucher
        product_voucher = Voucher.objects.filter(
            eligible_type='1',
            active_timestamp__lte=current_datetime,
            expiry_timestamp__gte=current_datetime).annotate(
            redeem_count=Count('redeem')).filter(redeem_count__gte=0).first()

        # try redeem on treatment
        self.assertFalse(product_voucher.verify_eligible_type(2))

        # set to 0 copied and try redeem
        product_voucher.copied = 0
        self.assertFalse(product_voucher.verify_max_redeem())

    def test_expired_voucher(self):
        # test expired redemption

        current_datetime = timezone.now()
        prev_datetime = current_datetime - timedelta(days=5)
        print(f"prev {prev_datetime}")
        # get product voucher
        product_voucher = Voucher.objects.filter(
            eligible_type='1',
            active_timestamp__lte=current_datetime,
            expiry_timestamp__gte=current_datetime).annotate(
            redeem_count=Count('redeem')).filter(redeem_count__gte=0).first()

        # set voucher to expired
        product_voucher.expiry_timestamp = prev_datetime
        self.assertTrue(product_voucher.verify_is_expired())

    def test_invalid_insert(self):
        voucher = Voucher()
        voucher.code = "123"
        voucher.discount_type = '$'
        voucher.discount_value = 10
        voucher.eligible_type = '1'
        voucher.copied = 2
        voucher.active_timestamp = timezone.now()
        voucher.expiry_timestamp = timezone.now() + timedelta(days=10)
        voucher.save()

        self.assertIsInstance(voucher, Voucher)
