from django.core.management.base import BaseCommand, CommandError
from items.models import Item, Price
from demosite.utils.class_define import ItemType
from random import randint, uniform
import datetime
import pytz

class Command(BaseCommand):
	help = 'create sample item data'

	def add_arguments(self, parser):
		parser.add_argument('total', type=int)

	def handle(self, *args, **kwargs):
		for x in ItemType:
			prefix = x.name[:1]
			for i in range(0, kwargs['total']):
				item = Item()
				item.sku = prefix+str(randint(1000000, 9999999))
				item.name = x.name[:3]+str(randint(1000, 9990))
				item.item_type = x.value
				item.active_timestamp = datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('Asia/Kuala_Lumpur'))
				item.expiry_timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('Asia/Kuala_Lumpur'))

				item.save()

				price = Price()
				price.item = item
				price.price = uniform(10.00, 200.00)
				price.effective_timestamp = datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('Asia/Kuala_Lumpur'))
				
				price.save()
