from bs4 import BeautifulSoup
from json import dumps, loads
from random import randint, random

from django.contrib.auth.models import User
from django.utils.six import BytesIO

from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.reverse import django_reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate

from assets.api_views import CowDetail, CowList
from assets.models import Age, Breed, BreedImage, Color, Cow
from assets.tests.utils import TestData, TestTime
from assets.views import IndexView

class TestCowListView(APITestCase):
    fixtures = ['age', 'breed', 'breedimage', 'color', 'user', 'cow']

    def setUp(self):
        self.data = {'purchased_by': TestData.get_random_user(),
                     'purchase_date': TestTime.get_purchase_date(),
                     'age': TestData.get_age(),
                     'breed': TestData.get_breed(),
                     'color': TestData.get_color(),
                     'image': TestData.get_image()}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.herd = Cow.objects.all()
        self.request = None
        self.url = django_reverse('assets:cow-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.herd = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowList.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_list_methods(),
                          response.get('allow'))
        #self.assertEquals(TestData.get_content_length(),
        #                  response.get('content-length'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
        url = django_reverse('assets:cow-list')
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowList.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('count',
                      data)
        self.assertIn('next',
                      data)
        self.assertIn('previous',
                      data)
        self.assertIn('results',
                      data)
        for cow in data['results']:
            for key in TestData.get_cow_keys():
                self.assertIn(key,
                              cow)

    def test_03_create(self):
        url = django_reverse('assets:cow-list')
        request = self.factory.post(path=self.url,
                                    data=dumps(self.data),
                                    content_type=TestData.get_format(),
                                    follow=False)
        force_authenticate(request,
                           user=self.user)
        request.POST = self.data
        self.assertTrue(self.user.is_authenticated)
        response = CowList.as_view()(request=request)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_cow_keys():
            self.assertIn(key,
                          data)
