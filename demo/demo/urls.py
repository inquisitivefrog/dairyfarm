from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

from demo.api_views import UserCreate, UserDetail
from demo.views import redirect

urlpatterns = [
    url(r'^$',
        redirect,
        name='redirect'),
    url(r'^auth/',
        include('rest_framework.urls')),
    url(r'^api/create_user/$',
        UserCreate.as_view(),
        name='user_create'),
    url(r'^api/users/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='user_detail'),
    url(r'^assets/', include('assets.urls',
                             namespace="assets")),
    path('admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
