from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from model_utils import Choices
from items.models import Item
from multiselectfield import MultiSelectField
from demosite.utils import DiscountType, ItemType

DIS_CHOICES = []
for d in DiscountType:
    DIS_CHOICES += Choices(d.value)

ITEM_CHOICES = []
ITEM_SUM = 0
for i in ItemType:
    ITEM_SUM += i.value
    ITEM_CHOICES += Choices((i.value, i.name))


class PatchedMultiSelectField(MultiSelectField):
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class Voucher(models.Model):
    """
    Redemption timestamp must between active and expiry
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
        return str(compare) in set(self.eligible_type)

    def verify_max_redeem(self):
        return self.copied > self.redeem_set.all().count()

    @staticmethod
    def verify_is_voucher(code):
        try:
            voucher = Voucher.objects.get(code=code.upper())
        except Voucher.DoesNotExist:
            voucher = None

        return voucher

    def __str__(self):
        return '%s' % (self.code)


class Redeem(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    redeem_timestamp = models.DateTimeField(blank=False, null=False)

    def __init__(self, *args, **kwargs):
        super(Redeem, self).__init__(*args, **kwargs)
