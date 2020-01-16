"""Model design for Vouchers

* Currently contain two diff type of voucher $ | %
"""

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from model_utils import Choices
from items.models import Item
from multiselectfield import MultiSelectField
from demosite.utils import DiscountType, ItemType
from django.utils import timezone

DIS_CHOICES = Choices()
for d in DiscountType:
    DIS_CHOICES += Choices(d.value)

ITEM_CHOICES = Choices()
ITEM_SUM = 0
for i in ItemType:
    ITEM_SUM += i.value
    ITEM_CHOICES += Choices((i.value, i.name))


class PatchedMultiSelectField(MultiSelectField):
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class Voucher(models.Model):
    """Voucher class design

    Parameters
    ----------
    code: Char field, length=10, ascii or digit
        Voucher code
    discount_type: Char field, length=1, % OR $
        Discount type for voucher
    discount_value: Float, decimal=2, min=0.01
        Percentage discount for % sign, max=100
        Dollar discount for $ sign
    eligible_type: Multi select box
        Determine voucher only eligible with what item type
    copied: Positive integer
        Redeemable count of particular voucher
    active_timestamp: Datetime
        Voucher valid start date
    expiry_timestamp: Datetime
        Voucher end date
    """

    code = models.CharField(
        max_length=10,
        unique=True,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9]{10}$',
                message='Space is not allow and Length has to be 10',
                code='invalid_code')])
    discount_type = models.CharField(
        max_length=1,
        choices=DIS_CHOICES,
        unique=False,
        blank=False,
        null=False)
    discount_value = models.FloatField(
        unique=False, blank=False, null=False, validators=[
            MinValueValidator(0.01)])
    eligible_type = PatchedMultiSelectField(
        choices=ITEM_CHOICES, null=False, blank=False)

    copied = models.PositiveIntegerField(
        unique=False,
        blank=False,
        null=False,
        default=1,
        validators=[
            MinValueValidator(1)])
    active_timestamp = models.DateTimeField(blank=False, null=False)
    expiry_timestamp = models.DateTimeField(blank=False, null=False)

    def __init__(self, *args, **kwargs):
        super(Voucher, self).__init__(*args, **kwargs)
        self.code = self.code.upper()

    def verify_eligible_type(self, compare):
        """

        Parameters
        ----------
        compare: str
            compare item type with voucher eligible type
        Returns
        -------
        Boolean
        """
        return str(compare) in set(self.eligible_type)

    def verify_max_redeem(self):
        # Verify is voucher fully utilized
        return self.copied > self.redeem_set.all().count()

    def verify_is_expired(self):
        # Verify is voucher due
        return self.expiry_timestamp <= timezone.now()

    @staticmethod
    def verify_is_voucher(code):
        """Verify if is valid voucher

        Parameters
        ----------
        code: str
            Metadata voucher code
        Returns
        -------
        Voucher model object | None
        """
        try:
            voucher = Voucher.objects.get(code=code.upper(),
                                          active_timestamp__lte=timezone.now())
        except Voucher.DoesNotExist:
            voucher = None

        return voucher

    def __str__(self):
        return f"{self.__class__.__name__}({self.code})"


class Redeem(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    redeem_timestamp = models.DateTimeField(blank=False, null=False)

    def __init__(self, *args, **kwargs):
        super(Redeem, self).__init__(*args, **kwargs)
