from bs4 import BeautifulSoup

from django.contrib.auth.models import User

from rest_framework.reverse import django_reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate

from assets.tests.utils import TestData, TestTime
from assets.views import IndexView

class TestIndexView(APITestCase):
    fixtures = ['user']

    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.url = django_reverse('assets:index')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.factory = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url)
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = IndexView.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_length(),
                          response.get('content-length'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_get(self):
        request = self.factory.get(path=self.url)
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = IndexView.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        response.render()
        soup = BeautifulSoup(response.content,
                             'html.parser')
        self.assertEquals('My Dairy Farm',
                          soup.title.string)
        self.assertEquals('/static/angular/angular.min.js',
                          soup.findAll('script')[0]['src'])
        self.assertEquals('/static/angular/angular-route.min.js',
                          soup.findAll('script')[1]['src'])
        self.assertEquals('/static/app.js',
                          soup.findAll('script')[2]['src'])
        self.assertEquals('farmApp',
                          soup.find('body')['ng-app'])
        self.assertEquals('AssetController',
                          soup.findAll('div')[0]['ng-controller'])
