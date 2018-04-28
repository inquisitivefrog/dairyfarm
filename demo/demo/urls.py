from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path

from demo.api_views import UserCreate, UserDetail
from demo.views import IndexView

urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='index'),
    url(r'^login/$',
        LoginView.as_view(),
        name='login'),
    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),
    url(r'^api/create_user/$',
        UserCreate.as_view(),
        name='user_create'),
    url(r'^api/users/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='user_detail'),
    url(r'^assets/',
        include('assets.urls',
                namespace="assets")),
    url(r'^summary/',
        include('summary.urls',
                namespace="summary")),
    path('admin/',
         admin.site.urls)
] + static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT)
