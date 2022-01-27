from django.urls import path

from .views import *

urlpatterns = [
    path('cart/', CartListAddView.as_view(), name='cart'),
    path('cart/<int:pk>', CartPutDeleteView.as_view(), name='cartItem'),
    path('order/', OrderListAddView.as_view(), name='cart'),
    path('order/<int:pk>', OrderPutDeleteView.as_view(), name='cartItem'),

]
