from django.urls import path, include
from django.conf.urls.static import static

from ..settings.base import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT

urlpatterns = [
    path('', include(('apps.core.urls', 'apps.core'), namespace='core')),
    path('account/', include(('apps.account.urls', 'apps.account'), namespace='account')),
    path('captcha/', include('captcha.urls')),

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
