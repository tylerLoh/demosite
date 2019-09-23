from django.db import models
from model_utils import Choices
from django.core.validators import RegexValidator, MinValueValidator
from utils.class_define import ItemType
from decimal import Decimal

TYPE_CHOICES = []
for d in ItemType:
	TYPE_CHOICES += Choices((d.value, d.name))

class Item(models.Model):
	sku = models.CharField(max_length=8, unique=True, blank=False, null=False,
		validators=[RegexValidator(
			r'^[a-zA-Z0-9]+$',
			message='Space is not allow',
			code='invalid_sku'
		)])
	name = models.CharField(max_length=25, unique=True, blank=False, null=False)
	item_type = models.IntegerField(choices=TYPE_CHOICES, blank=False, null=False)
	status = models.BooleanField(blank=False, null=False)
	# eligible = 
	active_timestamp = models.DateTimeField(blank=False, null=False)
	expiry_timestamp = models.DateTimeField(blank=False, null=False)
	
	def __init__(self, *args, **kwargs):
		super(Item, self).__init__(*args, **kwargs)

	def __str__(self):
		return '%s' % (self.sku)

class Price(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	price = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=6,
		validators=[MinValueValidator(Decimal('0.00'))])
	effective_timestamp = models.DateTimeField(blank=False, null=False)

	def __init__(self, *args, **kwargs):
		super(Price, self).__init__(*args, **kwargs)

	def __str__(self):
		return '%s $%.2f' % (self.item.sku, self.price)
