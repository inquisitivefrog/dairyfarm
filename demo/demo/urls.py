from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LoginView

from django.urls import include, path, re_path

from demo.api_views import UserCreate, UserDetail
from demo.views import contact, redirect, IndexView
from demo.views import ui_login, ui_logged_in, ui_logout

urlpatterns = [
    #url(r'^$',
    #    redirect,
    #    name='redirect'),
    re_path(r'^$',
        IndexView.as_view(),
        name='index'),
    re_path(r'^ui_login/$',
        ui_login,
        name='ui_login'),
    re_path(r'^ui_logged_in/$',
        ui_logged_in,
        name='ui_logged_in'),
    re_path(r'^ui_logout/$',
        ui_logout,
        name='ui_logout'),
    re_path(r'^login/$',
        LoginView.as_view(),
        name='login'),
    re_path(r'^logout/$',
        ui_logout,
        name='logout'),
    re_path(r'^contact/$',
        contact,
        name='contact'),
    re_path(r'^api/create_user/$',
        UserCreate.as_view(),
        name='user_create'),
    re_path(r'^api/users/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='user_detail'),
    re_path(r'^assets/',
        include('assets.urls',
                namespace="assets")),
    re_path(r'^summary/',
        include('summary.urls',
                namespace="summary")),
    path('admin/',
         admin.site.urls)
] + static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT)
