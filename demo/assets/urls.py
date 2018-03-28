from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from assets.api_views import CowDetail, CowList, CowListByMonth, CowListByYear
from assets.api_views import EventDetail, EventList
from assets.api_views import ExerciseDetail, ExerciseList, HealthRecordDetail
from assets.api_views import HealthRecordList, MilkDetail, MilkList
from assets.api_views import SeedDetail, SeedList
from assets.views import IndexView

app_name = 'assets'
urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='index'),
    url(r'^api/cows/$',
        CowList.as_view(),
        name='cow-list'),
    url(r'^api/cows/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        CowListByMonth.as_view(),
        name='cow-list-month'),
    url(r'^api/cows/(?P<year>[0-9]{4})/$',
        CowListByYear.as_view(),
        name='cow-list-year'),
    url(r'^api/cows/(?P<pk>\d+)/$',
        CowDetail.as_view(),
        name='cow-detail'),
    url(r'^api/events/$',
        EventList.as_view(),
        name='event-list'),
    url(r'^api/events/(?P<pk>\d+)/$',
        EventDetail.as_view(),
        name='event-detail'),
    url(r'^api/exercises/$',
        ExerciseList.as_view(),
        name='exercise-list'),
    url(r'^api/exercises/(?P<pk>\d+)/$',
        ExerciseDetail.as_view(),
        name='exercise-detail'),
    url(r'^api/healthrecords/$',
        HealthRecordList.as_view(),
        name='healthrecord-list'),
    url(r'^api/healthrecords/(?P<pk>\d+)/$',
        HealthRecordDetail.as_view(),
        name='healthrecord-detail'),
    url(r'^api/milk/$',
        MilkList.as_view(),
        name='milk-list'),
    url(r'^api/milk/(?P<pk>\d+)/$',
        MilkDetail.as_view(),
        name='milk-detail'),
    url(r'^api/seeds/$',
        SeedList.as_view(),
        name='seed-list'),
    url(r'^api/seeds/(?P<pk>\d+)/$',
        SeedDetail.as_view(),
        name='seed-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
