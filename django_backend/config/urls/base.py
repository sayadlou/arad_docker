from django.urls import path, include


urlpatterns = [
    path('', include(('apps.core.urls', 'apps.core'), namespace='core')),
    path('account/', include(('apps.account.urls', 'apps.account'), namespace='account')),
    path('blog/', include(('apps.blog.urls', 'apps.blog'), namespace='blog')),
    path('store/', include(('apps.store.urls', 'apps.store'), namespace='store')),
    path('learning/', include(('apps.learning.urls', 'apps.learning'), namespace='learning')),
    path('captcha/', include('captcha.urls')),
    path('contact_us/', include(('apps.contact_us.urls', 'apps.contact_us'), namespace='contact_us')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


