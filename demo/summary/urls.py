from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from summary.api_views import AnnualSummaryByClientView
from summary.api_views import MonthlySummaryByClientView

app_name = 'summary'
urlpatterns = [
    url(r'^api/annual/client/(?P<pk>\d+)/$',
        AnnualSummaryByClientView.as_view(),
        name='annual-client'),
    url(r'^api/annual/client/(?P<pk>\d+)/year/(?P<year>[0-9]{4})/$',
        AnnualSummaryByClientView.as_view(),
        name='annual-client-year'),
    url(r'^api/monthly/client/(?P<pk>\d+)/year/(?P<year>[0-9]{4})/$',
        MonthlySummaryByClientView.as_view(),
        name='monthly-client-year'),
    url(r'^api/monthly/client/(?P<pk>\d+)/year/(?P<year>[0-9]{4})/month/(?P<month>[0-9]{1,2})/$',
        MonthlySummaryByClientView.as_view(),
        name='monthly-client-year-month'),
]
