"""Base Form for Purchase page

Include collection of field, with all associated field type
"""

from django import forms
from django.core.validators import RegexValidator, MinValueValidator, \
    MaxValueValidator
from vouchers.models import Voucher, Redeem
from items.models import Item
from datetime import datetime


class PurchaseForm(forms.Form):
    """BaseForm class

    Attributes
    ----------
    max_message: str
        validation msg for max purchase amount
    min_message: str
        validation msg for min purchase
    quantity:  Interger Field
        min: 1
        max: 100
    voucher: Char Field
        max: 10 (Voucher model guid length)
    """
    max_message = "Max quantity for purchase 100"
    min_message = "Min quality for purchase 1"

    quantity = forms.IntegerField(label='Quantity',
                                  validators=[
                                      MaxValueValidator(
                                          100,
                                          message=max_message),
                                      MinValueValidator(
                                          1,
                                          message=min_message)
                                  ])
    voucher = forms.CharField(label='Voucher code', max_length=10,
                              required=False)

    def __init__(self, *args, **kwargs):
        # pop sku to self instance, first instance doesn't hold sku key
        self.sku = kwargs.pop('sku')
        super(PurchaseForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Validator hook doing any extra form-wide cleaning

        Returns
        -------
        Field cleaned data
        """
        cleaned_data = super(PurchaseForm, self).clean()
        cleaned_quantity = cleaned_data.get('quantity')
        cleaned_voucher = cleaned_data.get('voucher')

        if cleaned_voucher and len(cleaned_voucher) != 10:
            self.add_error('voucher', "Voucher code must be 10 characters")
        elif len(cleaned_voucher) == 10:
            voucher = Voucher.verify_is_voucher(cleaned_voucher)
            if voucher:
                item = Item.objects.get(sku=self.sku)
                if item and voucher.verify_eligible_type(item.item_type):
                    if voucher.verify_max_redeem():
                        pass
                    else:
                        self.add_error('voucher',
                                       "Voucher code has been fully redeemed")
                else:
                    self.add_error('voucher',
                                   "Voucher do not apply to this item")
            else:
                self.add_error('voucher', "Voucher code doesnt exist")

        return cleaned_data

    def save(self, item):
        """Form save flow design for Voucher model

        If purchased is with voucher, it will save redeem count for particular
        voucher code

        Parameters
        ----------
        item: Item model object
        """

        cleaned_data = self.cleaned_data
        cleaned_voucher = cleaned_data.get('voucher')

        if cleaned_voucher:
            voucher = Voucher.objects.get(code=cleaned_voucher.upper())
            redeem = Redeem()
            redeem.voucher = voucher
            redeem.item = item
            redeem.redeem_timestamp = datetime.now()
            redeem.save()
        pass
