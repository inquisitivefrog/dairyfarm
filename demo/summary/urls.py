from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from summary.api_views import AnnualSummary, MonthlySummary

app_name = 'summary'
urlpatterns = [
    url(r'^api/annual/(?P<year>[0-9]{4})/$',
        AnnualSummary.as_view(),
        name='annual'),
    url(r'^api/monthly/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        MonthlySummary.as_view(),
        name='monthly'),
]
