"""Model design for Item and Price chain

* Each Item can have many different Price (one-to-many).
* Use timestamp to control current running price, which means price can
pre-define

"""

from django.db import models
from model_utils import Choices
from django.core.validators import RegexValidator, MinValueValidator
from demosite.utils import ItemType
from decimal import Decimal
import hashlib
from random import randrange

# Choices class for model Field

TYPE_CHOICES = Choices()
for item in ItemType:
    TYPE_CHOICES += Choices((item.value, item.name))


class Item(models.Model):
    """Item model design

    Parameters
    ----------
    sku: Char Field
        Unique ascii & number max 8 length sku code
    name: Char Field
        Name of the item
    item_type: Interger Field
        Only allow single item type
    status: Boolean
        Activation status
    image_hash: hexadecimal digits
        Chain hash_image method to generate image hash string for img callback
    active_timestamp: DateTime
        Created/Show timestamp, active_timestamp < now < expiry_timestamp
    expiry_timestamp:
        Expired timestamp, will hide from views
    """

    sku = models.CharField(max_length=8, unique=True, blank=False, null=False,
                           validators=[RegexValidator(
                               r'^[a-zA-Z0-9]+$',
                               message='Space is not allow',
                               code='invalid_sku'
                           )])
    name = models.CharField(max_length=25, unique=True, blank=False, null=False)
    item_type = models.IntegerField(choices=TYPE_CHOICES, blank=False,
                                    null=False)
    status = models.BooleanField(blank=False, null=False, default=True)
    image_hash = models.CharField(max_length=32, null=True)
    active_timestamp = models.DateTimeField(blank=False, null=False)
    expiry_timestamp = models.DateTimeField(blank=False, null=False)

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        if self.image_hash is None:
            self.image_hash = self.hash_image()

    def hash_image(self):
        # hash using sku(unique), hash image string will be unique too
        return hashlib.md5(
            self.name.lower().encode('utf-8') + self.sku.lower().encode(
                'utf-8')).hexdigest()

    def image(self, size=100, default="identicon", rating="g"):
        # generate image from api for item using hash string
        url = "https://secure.gravatar.com/avatar"
        hash_call = self.hash_image()
        return f"{url}/{hash_call}?s={size}&d={default}&r={rating}"

    def __repr__(self):
        return f"{self.__class__.__name__}{self.sku}"


class Price(models.Model):
    """Price model design flow

    Attributes
    ----------
    item: Foreign Key
    price: Decimal
        Actual price value in two decimal point
    effective_timestamp: DateTime
        Effective selling price
    """

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(blank=False, null=False, decimal_places=2,
                                max_digits=6,
                                validators=[MinValueValidator(Decimal('0.00'))])
    effective_timestamp = models.DateTimeField(blank=False, null=False)

    def __init__(self, *args, **kwargs):
        super(Price, self).__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__} {self.item.sku} {self.price:.2f}"
