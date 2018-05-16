from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path

from demo.api_views import UserCreate, UserDetail
from demo.views import contact, redirect, IndexView
from demo.views import ui_login, ui_logged_in, ui_logout

urlpatterns = [
    #url(r'^$',
    #    redirect,
    #    name='redirect'),
    url(r'^$',
        IndexView.as_view(),
        name='index'),
    url(r'^ui_login/$',
        ui_login,
        name='ui_login'),
    url(r'^ui_logged_in/$',
        ui_logged_in,
        name='ui_logged_in'),
    url(r'^ui_logout/$',
        ui_logout,
        name='ui_logout'),
    url(r'^login/$',
        LoginView.as_view(),
        name='login'),
    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),
    url(r'^contact/$',
        contact,
        name='contact'),
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
