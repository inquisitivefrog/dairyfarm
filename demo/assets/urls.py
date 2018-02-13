from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from assets.api_views import CowDetail, CowList, EventDetail, EventList
from assets.api_views import ExerciseDetail, ExerciseList, HealthRecordDetail
from assets.api_views import HealthRecordList, MilkDetail, MilkList
from assets.api_views import PastureDetail, PastureList
from assets.views import IndexView

app_name = 'assets'
urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='index'),
    url(r'^api/cows/$',
        CowList.as_view(),
        name='cow-list'),
    url(r'^api/cows/(?P<pk>[0-9]+)/$',
        CowDetail.as_view(),
        name='cow-detail'),
    url(r'^api/events/$',
        EventList.as_view(),
        name='event-list'),
    url(r'^api/events/(?P<pk>[0-9]+)/$',
        EventDetail.as_view(),
        name='event-detail'),
    url(r'^api/exercises/$',
        ExerciseList.as_view(),
        name='exercise-list'),
    url(r'^api/exercises/(?P<pk>[0-9]+)/$',
        ExerciseDetail.as_view(),
        name='exercise-detail'),
    url(r'^api/healthrecord/$',
        HealthRecordList.as_view(),
        name='healthrecord-list'),
    url(r'^api/healthrecord/(?P<pk>[0-9]+)/$',
        HealthRecordDetail.as_view(),
        name='healthrecord-detail'),
    url(r'^api/milk/$',
        MilkList.as_view(),
        name='milk-list'),
    url(r'^api/milk/(?P<pk>[0-9]+)/$',
        MilkDetail.as_view(),
        name='milk-detail'),
    url(r'^api/pastures/$',
        PastureList.as_view(),
        name='pasture-list'),
    url(r'^api/pastures/(?P<pk>[0-9]+)/$',
        PastureDetail.as_view(),
        name='pasture-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
