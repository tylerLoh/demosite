from django.db import models
from model_utils import Choices
from django.core.validators import RegexValidator, MinValueValidator
from demosite.utils import ItemType
from decimal import Decimal
import hashlib
from random import randrange

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
	image_hash = models.CharField(max_length=32, null=True) 
	active_timestamp = models.DateTimeField(blank=False, null=False)
	expiry_timestamp = models.DateTimeField(blank=False, null=False)
	
	def __init__(self, *args, **kwargs):
		super(Item, self).__init__(*args, **kwargs)
		if self.image_hash is None:
			self.image_hash = self.image_hash()

	
	def image_hash(self):
		return hashlib.md5(self.name.lower().encode('utf-8') + self.sku.lower().encode('utf-8')).hexdigest()
	
	#generate some image for item
	def image(self, size=100, default='identicon', rating='g'):
		url = 'https://secure.gravatar.com/avatar'
		hash = self.image_hash()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
			url=url, hash=hash, size=size, default=default, rating=rating)

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
