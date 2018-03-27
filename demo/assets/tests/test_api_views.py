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

from assets.api_views import CowDetail, CowList, EventDetail, EventList
from assets.api_views import ExerciseDetail, ExerciseList, HealthRecordDetail
from assets.api_views import HealthRecordList, MilkDetail, MilkList
from assets.api_views import PastureDetail, PastureList
from assets.models import Action, Age, Breed, CerealHay, Color, Cow
from assets.models import Event, Exercise, GrassHay, HealthRecord, Illness
from assets.models import Injury, LegumeHay, Milk, Pasture, Region
from assets.models import Season, Status, Vaccine
from assets.tests.utils import TestData, TestTime
from assets.views import IndexView

class TestCowListView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow']

    def setUp(self):
        self.data = {'purchased_by': TestData.get_random_user(),
                     'purchase_date': TestTime.get_purchase_date(),
                     'age': TestData.get_age(),
                     'breed': 'Holstein',
                     'color': 'black_white'}
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
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
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
            for key in TestData.get_cow_read_keys():
                self.assertIn(key,
                              cow)

    def test_03_create(self):
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
        for key in TestData.get_cow_write_keys():
            self.assertIn(key,
                          data)

class TestCowDetailView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow']

    def setUp(self):
        self.data = {'purchased_by': TestData.get_random_user(),
                     'purchase_date': TestTime.get_purchase_date(),
                     'age': TestData.get_age(),
                     'breed': 'Holstein',
                     'color': 'black_white'}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.herd = Cow.objects.all()
        self.request = None
        self.pk = self.herd[0].id
        self.url = django_reverse('assets:cow-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.herd = None
        self.pk = None
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
        response = CowDetail.as_view()(request=request,
                                       pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_detail_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_retrieve(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_cow_read_keys():
            self.assertIn(key,
                          data)

    def test_03_full_update(self):
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn('rfid',
                      data)
        self.assertEqual(self.data['purchased_by'],
                      data['purchased_by'])
        self.assertEqual(self.data['purchase_date'],
                      data['purchase_date'])
        self.assertEqual(self.data['age'],
                      data['age'])
        self.assertEqual(self.data['breed'],
                      data['breed'])
        self.assertEqual(self.data['color'],
                      data['color'])
        self.assertIn('link',
                      data)

    def test_04_partial_update(self):
        data = {'age': self.data['age'],
                'breed': self.data['breed']}
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn('rfid',
                      data)
        self.assertIn('purchased_by',
                      data)
        self.assertIn('purchase_date',
                      data)
        self.assertEqual(self.data['age'],
                      data['age'])
        self.assertEqual(self.data['breed'],
                      data['breed'])
        self.assertIn('color',
                      data)
        self.assertIn('link',
                      data)

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=self.pk)
        self.assertEqual(204,
                         response.status_code)
        self.assertEqual('No Content',
                         response.reason_phrase)

class TestPastureListView(APITestCase):
    fixtures = ['cerealhay', 'grasshay', 'legumehay', 'region',
                'season', 'user', 'pasture']

    def setUp(self):
        fallow = False
        distance = TestData.get_distance()
        user = User.objects.get(username=TestData.get_random_user())
        cereals = CerealHay.objects.all()
        cereal = cereals[randint(0, len(cereals) - 1)]
        grasses = GrassHay.objects.all()
        grass = grasses[randint(0, len(grasses) - 1)]
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        regions = Region.objects.all()
        region = regions[randint(0, len(regions) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.data = {'fallow': fallow,
                     'distance': distance,
                     'plant_date': TestTime.convert_date(TestTime.get_date()),
                     'year': TestTime.get_year(),
                     'season': season.name,
                     'seeded_by': user.username,
                     'region': region.name,
                     'cereal_hay': cereal.name,
                     'grass_hay': grass.name,
                     'legume_hay': legume.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.url = django_reverse('assets:pasture-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        cereals = CerealHay.objects.all()
        self.assertLessEqual(1,
                             len(cereals))
        grasses = GrassHay.objects.all()
        self.assertLessEqual(1,
                             len(grasses))
        legumes = LegumeHay.objects.all()
        self.assertLessEqual(1,
                             len(legumes))
        seasons = Season.objects.all()
        self.assertLessEqual(4,
                             len(seasons))
        fields = Pasture.objects.all()
        self.assertLessEqual(1,
                             len(fields))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = PastureList.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_list_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = PastureList.as_view()(request=request)
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
        for field in data['results']:
            for key in TestData.get_pasture_read_keys():
                self.assertIn(key,
                              field)

    def test_03_create(self):
        request = self.factory.post(path=self.url,
                                    data=dumps(self.data),
                                    content_type=TestData.get_format(),
                                    follow=False)
        force_authenticate(request,
                           user=self.user)
        request.POST = self.data
        self.assertTrue(self.user.is_authenticated)
        response = PastureList.as_view()(request=request)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_pasture_write_keys():
            self.assertIn(key,
                          data)

class TestPastureDetailView(APITestCase):
    fixtures = ['cerealhay', 'grasshay', 'legumehay', 'region',
                'season', 'user', 'pasture']

    def setUp(self):
        fallow = False
        distance = TestData.get_distance()
        user = User.objects.get(username=TestData.get_random_user())
        cereals = CerealHay.objects.all()
        cereal = cereals[randint(0, len(cereals) - 1)]
        grasses = GrassHay.objects.all()
        grass = grasses[randint(0, len(grasses) - 1)]
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        regions = Region.objects.all()
        region = regions[randint(0, len(regions) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.data = {'fallow': fallow,
                     'distance': distance,
                     'year': TestTime.get_year(),
                     'season': season.name,
                     'seeded_by': user.username,
                     'region': region.name,
                     'cereal_hay': cereal.name,
                     'grass_hay': grass.name,
                     'legume_hay': legume.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.pk = Pasture.objects.get(pk=1).id
        self.url = django_reverse('assets:pasture-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        cereals = CerealHay.objects.all()
        self.assertLessEqual(1,
                             len(cereals))
        grasses = GrassHay.objects.all()
        self.assertLessEqual(1,
                             len(grasses))
        legumes = LegumeHay.objects.all()
        self.assertLessEqual(1,
                             len(legumes))
        seasons = Season.objects.all()
        self.assertLessEqual(4,
                             len(seasons))
        fields = Pasture.objects.all()
        self.assertLessEqual(1,
                             len(fields))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = PastureDetail.as_view()(request=request,
                                           pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_detail_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_retrieve(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = PastureDetail.as_view()(request=request,
                                           pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_pasture_read_keys():
            self.assertIn(key,
                          data)

    def test_03_full_update(self):
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = PastureDetail.as_view()(request=request,
                                           pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_pasture_write_keys():
            self.assertIn(key,
                          data)

    def test_04_partial_update(self):
        data = {'grass_hay': self.data['grass_hay'],
                'legume_hay': self.data['legume_hay']}
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = PastureDetail.as_view()(request=request,
                                           pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn('fallow',
                      data)
        self.assertIn('year',
                      data)
        self.assertIn('season',
                      data)
        self.assertIn('distance',
                      data)
        self.assertIn('seeded_by',
                      data)
        self.assertIn('cereal_hay',
                      data)
        self.assertEqual(self.data['grass_hay'],
                      data['grass_hay'])
        self.assertEqual(self.data['legume_hay'],
                      data['legume_hay'])
        self.assertIn('region',
                      data)
        self.assertIn('link',
                      data)

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = PastureDetail.as_view()(request=request,
                                           pk=self.pk)
        self.assertEqual(204,
                         response.status_code)
        self.assertEqual('No Content',
                         response.reason_phrase)

class TestEventListView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'action', 'event']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        actions = Action.objects.all()
        action = actions[randint(0, len(actions) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'action': action.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.url = django_reverse('assets:event-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        actions = Action.objects.all()
        self.assertLessEqual(1,
                             len(actions))
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        events = Event.objects.all()
        self.assertLessEqual(1,
                             len(events))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventList.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_list_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventList.as_view()(request=request)
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
        for event in data['results']:
            for key in TestData.get_event_read_keys():
                self.assertIn(key,
                              event)

    def test_03_create(self):
        request = self.factory.post(path=self.url,
                                    data=dumps(self.data),
                                    content_type=TestData.get_format(),
                                    follow=False)
        force_authenticate(request,
                           user=self.user)
        request.POST = self.data
        self.assertTrue(self.user.is_authenticated)
        response = EventList.as_view()(request=request)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_event_write_keys():
            self.assertIn(key,
                          data)

class TestEventDetailView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'action', 'event']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        actions = Action.objects.all()
        action = actions[randint(0, len(actions) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'action': action.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.pk = Event.objects.get(pk=1).id
        self.url = django_reverse('assets:event-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        actions = Action.objects.all()
        self.assertLessEqual(1,
                             len(actions))
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        events = Event.objects.all()
        self.assertLessEqual(1,
                             len(events))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_detail_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_retrieve(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_event_read_keys():
            self.assertIn(key,
                          data)

    def test_03_full_update(self):
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn(self.data['recorded_by'],
                      data['recorded_by'])
        self.assertIn(self.data['cow'],
                      data['cow'])
        self.assertEqual(self.data['action'],
                      data['action'])

    def test_04_partial_update(self):
        data = {'action': self.data['action']}
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn('recorded_by',
                      data)
        self.assertIn('cow',
                      data)
        self.assertEqual(self.data['action'],
                      data['action'])

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=self.pk)
        self.assertEqual(204,
                         response.status_code)
        self.assertEqual('No Content',
                         response.reason_phrase)

class TestExerciseListView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'cerealhay', 'grasshay', 'legumehay', 'region',
                'season', 'pasture', 'exercise']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        fields = Pasture.objects.all()
        pasture = fields[randint(0, len(fields) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        distance = TestData.get_distance()
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'pasture': pasture.region.id,
                     'distance': distance}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.url = django_reverse('assets:exercise-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        exercises = Exercise.objects.all()
        self.assertLessEqual(1,
                             len(exercises))
        fields = Pasture.objects.all()
        self.assertLessEqual(1,
                             len(fields))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseList.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_list_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseList.as_view()(request=request)
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
        for event in data['results']:
            for key in TestData.get_exercise_read_keys():
                self.assertIn(key,
                              event)

    def test_03_create(self):
        request = self.factory.post(path=self.url,
                                    data=dumps(self.data),
                                    content_type=TestData.get_format(),
                                    follow=False)
        force_authenticate(request,
                           user=self.user)
        request.POST = self.data
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseList.as_view()(request=request)
        #self.assertEqual(400, response.status_code)
        #self.assertEqual('Bad Request', response.reason_phrase)
        #response = response.render()
        #self.assertEqual('WTF', response.content)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_exercise_write_keys():
            self.assertIn(key,
                          data)

class TestExerciseDetailView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'cerealhay', 'grasshay', 'legumehay', 'region',
                'season', 'pasture', 'exercise']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        fields = Pasture.objects.all()
        pasture = fields[randint(0, len(fields) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        distance = TestData.get_distance()
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'pasture': pasture.region.id,
                     'distance': distance}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.pk = Exercise.objects.get(pk=1).id
        self.url = django_reverse('assets:exercise-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        exercises = Exercise.objects.all()
        self.assertLessEqual(1,
                             len(exercises))
        fields = Pasture.objects.all()
        self.assertLessEqual(1,
                             len(fields))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseDetail.as_view()(request=request,
                                            pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_detail_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_retrieve(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseDetail.as_view()(request=request,
                                            pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_exercise_read_keys():
            self.assertIn(key,
                          data)

    def test_03_full_update(self):
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseDetail.as_view()(request=request,
                                            pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn(self.data['recorded_by'],
                      data['recorded_by'])
        self.assertIn(self.data['cow'],
                      data['cow'])
        self.assertEqual(self.data['pasture'],
                      data['pasture'])
        self.assertEqual(self.data['distance'],
                      data['distance'])

    def test_04_partial_update(self):
        data = {'distance': self.data['distance']}
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseDetail.as_view()(request=request,
                                            pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn('recorded_by',
                      data)
        self.assertIn('cow',
                      data)
        self.assertIn('pasture',
                      data)
        self.assertEqual(self.data['distance'],
                      data['distance'])

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseDetail.as_view()(request=request,
                                            pk=self.pk)
        self.assertEqual(204,
                         response.status_code)
        self.assertEqual('No Content',
                         response.reason_phrase)

class TestMilkListView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow', 'milk']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        gallons = TestData.get_milk()
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'gallons': gallons}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.url = django_reverse('assets:milk-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        milk = Milk.objects.all()
        self.assertLessEqual(1,
                             len(milk))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MilkList.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_list_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MilkList.as_view()(request=request)
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
        for milk in data['results']:
            for key in TestData.get_milk_read_keys():
                self.assertIn(key,
                              milk)

    def test_03_create(self):
        request = self.factory.post(path=self.url,
                                    data=dumps(self.data),
                                    content_type=TestData.get_format(),
                                    follow=False)
        force_authenticate(request,
                           user=self.user)
        request.POST = self.data
        self.assertTrue(self.user.is_authenticated)
        response = MilkList.as_view()(request=request)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_milk_write_keys():
            self.assertIn(key,
                          data)

class TestMilkDetailView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow', 'milk']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        gallons = TestData.get_milk()
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'gallons': gallons}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.pk = Milk.objects.get(pk=1).id
        self.url = django_reverse('assets:milk-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        milk = Milk.objects.all()
        self.assertLessEqual(1,
                             len(milk))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MilkDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_detail_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_retrieve(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MilkDetail.as_view()(request=request,
                                            pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_milk_read_keys():
            self.assertIn(key,
                          data)

    def test_03_full_update(self):
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MilkDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn(self.data['recorded_by'],
                      data['recorded_by'])
        self.assertIn(self.data['cow'],
                      data['cow'])
        self.assertEqual(self.data['gallons'],
                      data['gallons'])

    def test_04_partial_update(self):
        data = {'gallons': self.data['gallons']}
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MilkDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn('recorded_by',
                      data)
        self.assertIn('cow',
                      data)
        self.assertEqual(self.data['gallons'],
                      data['gallons'])

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MilkDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(204,
                         response.status_code)
        self.assertEqual('No Content',
                         response.reason_phrase)

class TestHealthRecordListView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'illness', 'injury', 'status', 'vaccine', 'healthrecord']

    def setUp(self):
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        illnesses = Illness.objects.all()
        illness = illnesses[randint(0, len(illnesses) - 1)]
        injuries = Injury.objects.all()
        injury = injuries[randint(0, len(injuries) - 1)]
        statuses = Status.objects.all()
        status = statuses[randint(0, len(statuses) - 1)]
        user = User.objects.get(username=TestData.get_random_user())
        vaccines = Vaccine.objects.all()
        vaccine = vaccines[randint(0, len(vaccines) - 1)]
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                      'temperature': TestData.get_temp(),
                      'respiratory_rate': TestData.get_resp(),
                      'heart_rate': TestData.get_hr(),
                      'blood_pressure': TestData.get_bp(),
                      'weight': TestData.get_weight(),
                      'body_condition_score': TestData.get_bcs(),
                      'status': status.name,
                      'illness': illness.diagnosis,
                      'injury': injury.diagnosis,
                      'vaccine': vaccine.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.url = django_reverse('assets:healthrecord-list')
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
        illnesses = Illness.objects.all()
        self.assertLessEqual(1,
                             len(illnesses))
        injuries = Injury.objects.all()
        self.assertLessEqual(1,
                             len(injuries))
        statuses = Status.objects.all()
        self.assertLessEqual(1,
                             len(statuses))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))
        vaccines = Vaccine.objects.all()
        self.assertLessEqual(1,
                             len(vaccines))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = HealthRecordList.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_list_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = HealthRecordList.as_view()(request=request)
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
        for record in data['results']:
            for key in TestData.get_hr_read_keys():
                self.assertIn(key,
                              record)

    def test_03_create(self):
        request = self.factory.post(path=self.url,
                                    data=dumps(self.data),
                                    content_type=TestData.get_format(),
                                    follow=False)
        force_authenticate(request,
                           user=self.user)
        request.POST = self.data
        self.assertTrue(self.user.is_authenticated)
        response = HealthRecordList.as_view()(request=request)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_hr_write_keys():
            self.assertIn(key,
                          data)

class TestHealthRecordDetailView(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'illness', 'injury', 'status', 'vaccine', 'healthrecord']

    def setUp(self):
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        illnesses = Illness.objects.all()
        illness = illnesses[randint(0, len(illnesses) - 1)]
        injuries = Injury.objects.all()
        injury = injuries[randint(0, len(injuries) - 1)]
        statuses = Status.objects.all()
        status = statuses[randint(0, len(statuses) - 1)]
        user = User.objects.get(username=TestData.get_random_user())
        vaccines = Vaccine.objects.all()
        vaccine = vaccines[randint(0, len(vaccines) - 1)]
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'temperature': TestData.get_temp(),
                     'respiratory_rate': TestData.get_resp(),
                     'heart_rate': TestData.get_hr(),
                     'blood_pressure': TestData.get_bp(),
                     'weight': TestData.get_weight(),
                     'body_condition_score': TestData.get_bcs(),
                     'status': status.name,
                     'illness': illness.diagnosis,
                     'injury': injury.diagnosis,
                     'vaccine': vaccine.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.request = None
        self.pk = HealthRecord.objects.get(pk=1).id
        self.url = django_reverse('assets:healthrecord-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
        self.request = None
        self.user = None

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        illnesses = Illness.objects.all()
        self.assertLessEqual(1,
                             len(illnesses))
        injuries = Injury.objects.all()
        self.assertLessEqual(1,
                             len(injuries))
        statuses = Status.objects.all()
        self.assertLessEqual(1,
                             len(statuses))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))
        vaccines = Vaccine.objects.all()
        self.assertLessEqual(1,
                             len(vaccines))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = HealthRecordDetail.as_view()(request=request,
                                                pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_detail_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_retrieve(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = HealthRecordDetail.as_view()(request=request,
                                                pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_hr_read_keys():
            self.assertIn(key,
                          data)

    def test_03_full_update(self):
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = HealthRecordDetail.as_view()(request=request,
                                                pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        for key in TestData.get_hr_write_keys():
            self.assertIn(key,
                          data)

    def test_04_partial_update(self):
        data = {'temperature': self.data['temperature'],
                'blood_pressure': self.data['blood_pressure']}
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = HealthRecordDetail.as_view()(request=request,
                                                pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertIn('id',
                      data)
        self.assertIn('recorded_by',
                      data)
        self.assertIn('cow',
                      data)
        self.assertEqual(self.data['temperature'],
                      data['temperature'])
        self.assertIn('respiratory_rate',
                      data)
        self.assertIn('heart_rate',
                      data)
        self.assertEqual(self.data['blood_pressure'],
                      data['blood_pressure'])
        self.assertIn('weight',
                      data)
        self.assertIn('body_condition_score',
                      data)
        self.assertIn('status',
                      data)
        self.assertIn('illness',
                      data)
        self.assertIn('injury',
                      data)
        self.assertIn('vaccine',
                      data)

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = HealthRecordDetail.as_view()(request=request,
                                                pk=self.pk)
        self.assertEqual(204,
                         response.status_code)
        self.assertEqual('No Content',
                         response.reason_phrase)

