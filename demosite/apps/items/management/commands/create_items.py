"""Django command to create sample data for Item and Price Model

This command allows user to create sample data for Item and Price Model.
    python manage.py create_items [int]
"""
from django.core.management.base import BaseCommand, CommandError
from items.models import Item, Price
from demosite.utils.class_define import ItemType
from random import randint, uniform
from datetime import datetime
from pytz import timezone


class Command(BaseCommand):
    """A class to inherit Django BaseCommand

    Attributes
    ----------
    help: str
        A message to print out using -h option

    Methods
    -------
    add_arguments(parser)
        Entry point for subclassed commands to add custom arguments.
    handle()
    """
    help = "Create sample item data"

    def add_arguments(self, parser):
        # add total parser with int input
        parser.add_argument('total', type=int)

    def handle(self, *args, **kwargs):
        """Loop thru Enum object ItemType and create sample data

        Eg. For total = 10 will create 10 sample Item data into db
        """
        for x in ItemType:
            prefix = x.name[:1]
            for i in range(0, kwargs['total']):
                item = Item()
                item.sku = prefix + str(randint(1000000, 9999999))
                item.name = x.name[:3] + str(randint(1, 99909990))
                item.item_type = x.value
                item.active_timestamp = datetime(2019, 1, 1, 0, 0, 0,
                                                 tzinfo=timezone(
                                                     "Asia/Kuala_Lumpur"))
                item.expiry_timestamp = datetime(2020, 1, 1, 0, 0, 0,
                                                 tzinfo=timezone(
                                                     "Asia/Kuala_Lumpur"))

                item.save()

                price = Price()
                price.item = item
                price.price = uniform(10.00, 200.00)
                price.effective_timestamp = datetime(2019, 1, 1, 0, 0,
                                                     0,
                                                     tzinfo=timezone(
                                                         "Asia/Kuala_Lumpur"))

                price.save()
