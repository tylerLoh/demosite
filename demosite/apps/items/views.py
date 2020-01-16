"""Voucher views

for more information about views please check
https://docs.djangoproject.com/en/3.0/topics/http/views/
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import FormView
from items.models import Item, Price
from demosite.utils import ItemType
from django.utils import timezone
from . import forms


class HomePageView(View):
    """Home page view page

    Landing page will be always is get request
    """

    def get(self, request):
        """ handle get request method from view

        Returns
        -------
            render view for product and treatments
        """

        # load valid products
        all_products = Item.objects.filter(
            item_type=ItemType.PRODUCT.value,
            active_timestamp__lte=timezone.now(),
            expiry_timestamp__gte=timezone.now()
        )

        # load valid treatments
        all_treatments = Item.objects.filter(
            item_type=ItemType.TREATMENT.value,
            active_timestamp__lte=timezone.now(),
            expiry_timestamp__gte=timezone.now()
        )

        return render(request, 'home_page.html', {
            "products": all_products,
            "treatments": all_treatments
        })


class ItemView(FormView):
    """Particular Item View Class inherit with Form View

    Populate purchase form into item view

    Parameters
    ----------
    template_name: str, template path
        Override template path for the view
    form_class: Form Class
        Form to populate
    success_url: url
        A lazy evaluated callable for url, is to control success submission
        callback url
    """

    template_name = "item/item.html"
    form_class = forms.PurchaseForm
    success_url = reverse_lazy('home_page')

    def get_form_kwargs(self):
        """ Override method to mod/add new kwargs

        Returns
        -------
        kwargs
            To add sku keyword args for form_class object
        """
        kw = super(ItemView, self).get_form_kwargs()
        kw['sku'] = self.kwargs['sku']
        return kw

    def get_context_data(self, **kwargs):
        # override Form view get_context_data, add new context
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
        # Invalid handle
        return super(ItemView, self).form_invalid(form)

    def form_valid(self, form):
        # Valid submissin handle
        sku = self.kwargs['sku']
        item = Item.objects.get(sku=sku)
        form.save(item)

        return super(ItemView, self).form_valid(form)
