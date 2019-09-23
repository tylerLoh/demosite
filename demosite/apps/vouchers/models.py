from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from model_utils import Choices
from utils.class_define import DiscountType

TYPE_CHOICES = []
for d in DiscountType:
	TYPE_CHOICES += Choices(d.value)

class Voucher(models.Model):
	'''
	Redemption timestamp must between active and expiry
	'''
	code = models.CharField(max_length=10, unique=True, blank=False, null=False,
		validators=[RegexValidator(
			r'^[a-zA-Z0-9]+$',
			message='Space is not allow',
			code='invalid_code'
		)])
	discount_type = models.CharField(max_length=1, choices=TYPE_CHOICES, unique=False, blank=False, null=False)
	discount_value = models.IntegerField(unique=False, blank=False, null=False)
	# eligible = 
	active_timestamp = models.DateTimeField(blank=False, null=False)
	expiry_timestamp = models.DateTimeField(blank=False, null=False)

	def __init__(self, *args, **kwargs):
		super(Voucher, self).__init__(*args, **kwargs)

	def __str__(self):
		return '<Voucher code:%r, disount:%i(%r)>' % (self.code, self.discount_value, self.discount_type)
