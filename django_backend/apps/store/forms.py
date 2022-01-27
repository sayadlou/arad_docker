from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import CartItem


class CartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'quantity', 'content_type', 'object_pk', ]

    def clean(self):
        cleaned_data = super().clean()
        try:
            product = cleaned_data['content_type'].model_class().objects.get(pk=cleaned_data['object_pk'])
        except:
            raise ValidationError(_("product didn't find"))
        try:
            if cleaned_data['quantity'] > product.max_order_quantity:
                raise ValidationError(_("quantity is more than allowed value"))
            if cleaned_data['quantity'] < product.min_order_quantity:
                raise ValidationError(_("quantity is less than allowed value"))
        except KeyError:
            raise ValidationError(_("quantity is not valid"))

    def save_or_update(self):
        content_type_exists = CartItem.objects.filter(content_type=self.cleaned_data['content_type']).exists()
        object_pk_exists = CartItem.objects.filter(object_pk=self.cleaned_data['object_pk']).exists()
        if content_type_exists and object_pk_exists:
            data = CartItem.objects.get(object_pk=self.cleaned_data['object_pk'],
                                        content_type=self.cleaned_data['content_type'])
            data.quantity += self.cleaned_data['quantity']
            data.save()
        else:
            self.save()
