from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from summary.api_views import AnnualSummaryByClientView
from summary.api_views import MonthlySummaryByClientView

app_name = 'summary'
urlpatterns = [
    re_path(r'^api/annual/client/(?P<pk>\d+)/$',
        AnnualSummaryByClientView.as_view(),
        name='annual-client'),
    re_path(r'^api/annual/client/(?P<pk>\d+)/year/(?P<year>[0-9]{4})/$',
        AnnualSummaryByClientView.as_view(),
        name='annual-client-year'),
    re_path(r'^api/monthly/client/(?P<pk>\d+)/year/(?P<year>[0-9]{4})/$',
        MonthlySummaryByClientView.as_view(),
        name='monthly-client-year'),
    re_path(r'^api/monthly/client/(?P<pk>\d+)/year/(?P<year>[0-9]{4})/month/(?P<month>[0-9]{1,2})/$',
        MonthlySummaryByClientView.as_view(),
        name='monthly-client-year-month'),
]
