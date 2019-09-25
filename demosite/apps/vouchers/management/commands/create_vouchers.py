from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from vouchers.models import Voucher
from model_utils import Choices
from demosite.utils.class_define import ItemType, DiscountType
from random import randint, uniform
import datetime
import pytz

class Command(BaseCommand):
	help = 'create sample voucher data'

	def handle(self, *args, **kwargs):
		for x in DiscountType:
			count = 1
			for i in ItemType:
				try:
					voucher = Voucher()
					voucher.code = i.name[:5] + '0000' + str(count)
					voucher.discount_type = x.value
					voucher.discount_value = (10 if x.value == '%' else 30)
					voucher.eligible_type = str(i.value)
					voucher.copied = 2
					voucher.active_timestamp = datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('Asia/Kuala_Lumpur'))
					voucher.expiry_timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('Asia/Kuala_Lumpur'))

					voucher.save()
					count = count + 1
				except IntegrityError as e: 
					pass