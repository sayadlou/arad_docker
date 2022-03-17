from decimal import Decimal
from pprint import pprint
import requests
import json
from uuid import uuid4
import logging

from azbankgateways import bankfactories
from azbankgateways.exceptions import AZBankGatewaysException
from azbankgateways.models import BankType
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.utils.translation import gettext as _

from .forms import CartItemForm
from ..store.models import CartItem, Order, OrderItem, Payment

logger = logging.getLogger(__name__)


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


class PaymentListAddView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        payments = Payment.objects.filter(owner=request.user)
        context = {'payments': payments, 'has_payments': payments.exists()}
        return render(request=self.request, template_name="store/payments.html", context=context)

    def post(self, request, *args, **kwargs):
        order_id = request.POST['order_id']
        order = get_object_or_404(Order, owner=request.user, pk=order_id)

        # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
        user_mobile_number = '+989112221234'  # اختیاری

        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create(
                BankType.ZARINPAL)  # or factory.create(bank_models.BankType.BMI) or set identifier
            bank.set_request(request)
            bank.set_amount(int(order.total_price))
            # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
            bank.set_client_callback_url(reverse('callback'))
            bank.set_mobile_number(order.owner.mobile)

            # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
            # پرداخت برقرار کنید.
            bank_record = bank.ready()

            # هدایت کاربر به درگاه بانک
            return bank.redirect_gateway()
        except AZBankGatewaysException as e:
            logging.critical(e)
            # TODO: redirect to failed page.
            raise e


class PaymentConfirmView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, owner=request.user, pk=kwargs['pk'])
        if request.GET['Status'] and request.GET['Status'] == 'OK':
            pass
        else:
            pass
        return HttpResponse("salam")
