import debug_toolbar
from django.urls import path, include

from .base import urlpatterns

urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
]
ROOT_URLCONF = 'config.urls.local'
