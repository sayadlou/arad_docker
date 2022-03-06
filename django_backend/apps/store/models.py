from decimal import Decimal
from uuid import uuid4

from django.db import models
from django.db.models import Sum, Func, F, Count
from django.utils.translation import ugettext_lazy as _

from ..account.models import UserProfile


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    max_order_quantity = models.DecimalField(max_digits=12, decimal_places=0)
    min_order_quantity = models.DecimalField(max_digits=12, decimal_places=0)
    purchaser = models.ManyToManyField(UserProfile)

    def __str__(self):
        return f"{self.title}"


class Cart(models.Model):
    CART_STATUS_WAITING = 'W'
    CART_STATUS_TRANSFERRED = 'T'
    CART_STATUS_FAILED = 'F'
    CART_STATUS_CHOICES = [
        (CART_STATUS_WAITING, 'Pending'),
        (CART_STATUS_TRANSFERRED, 'Transferred'),
        (CART_STATUS_FAILED, 'Failed')
    ]
    owner = models.OneToOneField(UserProfile, on_delete=models.RESTRICT)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=CART_STATUS_CHOICES, max_length=20, default=CART_STATUS_WAITING)
    status_change_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ('id',)

    def __str__(self):
        return self.owner.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # objects = ItemManager()

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
        ordering = ('id',)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
        ordering = ('id',)

    # def __unicode__(self):
    #     return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    # @property
    # def product(self):
    #     return self.content_type.get_object_for_this_type(pk=self.object_pk)
    #
    # @product.setter
    # def product(self, product):
    #     self.content_type = Product.objects.get_for_model(type(product))
    #     self.object_pk = product.pk


class Order(models.Model):
    ORDER_STATUS_WAITING = 'W'
    ORDER_STATUS_TRANSFERRED = 'T'
    ORDER_STATUS_PAYED = 'P'
    ORDER_STATUS_FAILED = 'F'
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_WAITING, 'Waiting'),
        (ORDER_STATUS_TRANSFERRED, 'Payed'),
        (ORDER_STATUS_PAYED, 'Transferred'),
        (ORDER_STATUS_FAILED, 'Failed')
    ]
    owner = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20, default=ORDER_STATUS_WAITING)
    status_change_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order')
        ordering = ('id',)

    @property
    def total_price(self):
        sum = 0
        for item in self.orderitem_set.all():
            sum += item.product.price * item.quantity
        return sum

    def __str__(self):
        return f"order of {self.owner.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
        ordering = ('id',)

    # def __unicode__(self):
    #     return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    # @property
    # def product(self):
    #     return self.content_type.get_object_for_this_type(pk=self.object_pk)
    #
    # @product.setter
    # def product(self, product):
    #     self.content_type = Product.objects.get_for_model(type(product))
    #     self.object_pk = product.pk
