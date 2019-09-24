from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import FormView
from items.models import Item, Price
from demosite.utils import ItemType
from datetime import datetime
from . import forms

class HomePageView(View):

	def get(self, request):
		all_products = Item.objects.filter(
			item_type=ItemType.PRODUCT.value,
			active_timestamp__lte=datetime.now(),
			expiry_timestamp__gte=datetime.now()
			)

		all_treatments = Item.objects.filter(item_type=ItemType.TREATMENT.value)

		return render(request, 'home_page.html', {
			"products" : all_products,
			"treatments" : all_treatments
		})

class ItemView(FormView):
	template_name = 'item/item.html'
	form_class = forms.PurchaseForm
	success_url = reverse_lazy('home_page')

	def get_context_data(self, **kwargs):
		context = super(ItemView, self).get_context_data(**kwargs)
		sku = self.kwargs['sku']
		item = Item.objects.get(sku=sku)
		price = item.price_set.order_by('-effective_timestamp')[:1].first()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context['form'] = form
		context['price'] = price
		context['item'] = item
		
		return context

	def form_invalid(self, form):
		form.save()
		return super(ItemView, self).form_invalid(form)

	def form_valid(self, form):
		return super(ItemView, self).form_valid(form)