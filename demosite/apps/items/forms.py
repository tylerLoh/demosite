from django import forms
from django.core.validators import RegexValidator, MinValueValidator
from vouchers.models import Voucher, Redeem

class PurchaseForm(forms.Form):
	quantity = forms.IntegerField(label='Quantity', min_value=1)
	voucher  = forms.CharField(label='Voucher code', max_length=10)

	def clean(self):
		cleaned_data = super(PurchaseForm, self).clean()
		quantity = cleaned_data.get('quantity')
		voucher = cleaned_data.get('voucher')

		if not quantity:
			raise forms.ValidationError("Invalid Quantity")

		if voucher:
			is_voucher = Voucher.objects.get(code=voucher)
			if is_voucher is None:
				raise forms.ValidationError("Voucher code doesnt exist")

	def save(self):
		pass