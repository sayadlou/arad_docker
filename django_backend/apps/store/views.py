import json
from decimal import Decimal
from pprint import pprint
import requests

from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.utils.translation import gettext as _

from .forms import CartItemForm
from ..store.models import CartItem, Order, OrderItem


def print_attributes(obj):
    def attributes(obj):
        from inspect import getmembers
        from types import FunctionType
        disallowed_names = {
            name for name, value in getmembers(type(obj))
            if isinstance(value, FunctionType)}
        return {
            name: getattr(obj, name) for name in dir(obj)
            if name[0] != '_' and name not in disallowed_names and hasattr(obj, name)}


class CartListAddView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {'cart': request.user.cart}
        cart_has_item = CartItem.objects.filter(cart=request.user.cart).exists()
        context['cart_has_item'] = cart_has_item
        if cart_has_item:
            context['cart_item'] = CartItem.objects.filter(cart=request.user.cart).order_by('id')
            cart_sum = 0
            for item in context['cart_item']:
                cart_sum += item.product.price * Decimal(item.quantity)
            context['cart_sum'] = cart_sum
        return render(request=self.request, template_name="store/cart.html", context=context)

    def post(self, request, *args, **kwargs):
        post_copy = request.POST.copy()
        post_copy['cart'] = self.request.user.cart
        form = CartItemForm(data=post_copy)
        if form.is_valid():
            messages.success(request, _('product added to cart'))
            form.save_or_update()
        else:
            for key in form.errors:
                for error in form.errors[key]:
                    messages.error(request, error)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CartPutDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=kwargs['pk'])
        post_copy = request.POST.copy()
        post_copy['cart'] = self.request.user.cart
        form = CartItemForm(data=post_copy, instance=cart_item)
        if form.is_valid():
            messages.success(request, _('product updated'))
            form.save_or_update()
        else:
            for key in form.errors:
                for error in form.errors[key]:
                    messages.error(request, error)
        return redirect(reverse('store:cart'), permanent=True)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(CartItem, pk=kwargs['pk'])
        if request.user.cart.pk == obj.cart.pk:
            obj.delete()
            return HttpResponse("deleted")
        else:
            return HttpResponse(status=404)


class OrderListAddView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(owner=request.user)
        context = {'orders': orders, 'has_order': orders.exists()}
        return render(request=self.request, template_name="store/orders.html", context=context)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        cart = request.user.cart
        order_items = list()
        new_order = Order.objects.create(owner=request.user, status='W')
        for item in cart.cartitem_set.all():
            order_items.append(
                OrderItem(
                    order=new_order,
                    quantity=item.quantity,
                    product=item.product,
                )
            )
        OrderItem.objects.bulk_create(order_items, batch_size=20)
        cart.cartitem_set.all().delete()
        return redirect(reverse('store:order_item', kwargs={'pk': new_order.id}), permanent=True)


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, owner=request.user, pk=kwargs["pk"])
        context = {'order': order}
        return render(request=request, template_name="store/order.html", context=context)


def go_to_gateway_view(request):
    data = {
        "merchant_id": "1344b5d4-0048-11e8-94db-005056a205be",
        "amount": 10000,
        "callback_url": "http://yoursite.com/ver",
        "description": "افزایش اعتبار کاربر شماره ۱۱۳۴۶۲۹"
    }
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
    response = requests.post('https://api.zarinpal.com/pg/v4/payment/request.json', data=json.dumps(data),
                             headers=headers)
    response_data = response.json()
    if response.status_code == 200 and response_data["data"].get('authority',None):
        if response_data["data"].get('code',None) == 100:
            return redirect(f'https://www.zarinpal.com/pg/StartPay/{response_data["data"]["authority"]}')
        #todo : add log
    return HttpResponseBadRequest
