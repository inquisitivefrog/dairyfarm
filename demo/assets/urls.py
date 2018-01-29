from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from assets.api_views import AgeDetail, AgeList, BreedDetail, BreedList
from assets.api_views import ColorDetail, ColorList, CowDetail, CowList
from assets.api_views import ImageDetail, ImageList
from assets.views import IndexView

app_name = 'assets'
urlpatterns = [
    url(r'^$',
        IndexView.as_view(),
        name='index'),
    url(r'^api/ages/$',
        AgeList.as_view(),
        name='age_list'),
    url(r'^api/ages/(?P<pk>[0-9]+)/$',
        AgeDetail.as_view(),
        name='age_detail'),
    url(r'^api/breeds/$',
        BreedList.as_view(),
        name='breed_list'),
    url(r'^api/breeds/(?P<pk>[0-9]+)/$',
        BreedDetail.as_view(),
        name='breed_detail'),
    url(r'^api/colors/$',
        ColorList.as_view(),
        name='color_list'),
    url(r'^api/colors/(?P<pk>[0-9]+)/$',
        ColorDetail.as_view(),
        name='color_detail'),
    url(r'^api/cows/$',
        CowList.as_view(),
        name='cow_list'),
    url(r'^api/cows/(?P<pk>[0-9]+)/$',
        CowDetail.as_view(),
        name='cow_detail'),
    url(r'^api/images/$',
        ImageList.as_view(),
        name='image_list'),
    url(r'^api/images/(?P<pk>[0-9]+)/$',
        ImageDetail.as_view(),
        name='image_detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
