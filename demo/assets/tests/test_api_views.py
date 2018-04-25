from json import dumps
from random import randint

from django.contrib.auth.models import User
from django.utils.six import BytesIO

from rest_framework.parsers import JSONParser
from rest_framework.reverse import django_reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate

from assets.api_views import CowDetail, CowList, CowListByMonth, CowListByYear
from assets.api_views import EventDetail, EventList, ExerciseDetail
from assets.api_views import ExerciseList, HealthRecordDetail
from assets.api_views import HealthRecordList, MilkDetail, MilkList
from assets.api_views import SeedDetail, SeedList
from assets.models import Action, Age, Breed, CerealHay, Client, Color, Cow
from assets.models import Event, Exercise, GrassHay, HealthRecord, Illness
from assets.models import Injury, LegumeHay, Milk, Pasture
from assets.models import Season, Seed, Status, Treatment, Vaccine
from assets.tests.utils import TestData, TestTime
from assets.views import IndexView

class TestCowListView(APITestCase):
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow']

    def setUp(self):
        client = Client.objects.get(pk=1)
        self.data = {'purchased_by': TestData.get_random_user(),
                     'purchase_date': TestTime.get_purchase_date(),
                     'age': TestData.get_age(),
                     'breed': 'Holstein',
                     'client': client.name, 
                     'color': 'black_white'}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.herd = Cow.objects.all()
        self.url = django_reverse('assets:cow-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.herd = None
        self.user = None

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(1,
                             len(clients))
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

class TestCowListByMonthView(APITestCase):
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow']

    def setUp(self):
        self.year = '2015'
        self.month = '01'
        client = Client.objects.get(pk=1)
        self.data = {'purchased_by': TestData.get_random_user(),
                     'purchase_date': TestTime.get_purchase_date(),
                     'age': TestData.get_age(),
                     'breed': 'Holstein',
                     'client': client.name,
                     'color': 'black_white'}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.herd = Cow.objects.all()
        self.url = django_reverse('assets:cow-list-month',
                                  args=(self.year, self.month))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.year = None
        self.month = None
        self.data = None
        self.factory = None
        self.herd = None
        self.url = None
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
        response = CowListByMonth.as_view()(request=request)
        if not response.is_rendered:
             response = response.render()
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_methods(),
                          response.get('allow'))
        self.assertEquals('application/json',
                          response.get('content-type'))
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual('Cow List By Month',
                         data['name'])
        self.assertEqual('',
                         data['description'])
        self.assertEqual(['application/json', 'text/html'],
                         data['renders'])
        parses = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']
        self.assertEqual(parses,
                         data['parses'])

    def test_02_list_no_args_kwargs(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowListByMonth.as_view()(request=request)
        if not response.is_rendered:
             response = response.render()
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

    def test_03_list_kwargs(self):
        kwargs = {'year': self.year, 'month': self.month}
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowListByMonth.as_view()(request=request, **kwargs)
        if not response.is_rendered:
             response = response.render()
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

class TestCowListByYearView(APITestCase):
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow']

    def setUp(self):
        self.year = '2015'
        client = Client.objects.get(pk=1)
        self.data = {'purchased_by': TestData.get_random_user(),
                     'purchase_date': TestTime.get_purchase_date(),
                     'age': TestData.get_age(),
                     'breed': 'Holstein',
                     'client': client.name,
                     'color': 'black_white'}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.herd = Cow.objects.all()
        self.url = django_reverse('assets:cow-list-year',
                                  args=(self.year,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.year = None
        self.data = None
        self.factory = None
        self.herd = None
        self.url = None
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
        response = CowListByYear.as_view()(request=request)
        if not response.is_rendered:
             response = response.render()
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_methods(),
                          response.get('allow'))
        self.assertEquals('application/json',
                          response.get('content-type'))
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual('Cow List By Year',
                         data['name'])
        self.assertEqual('',
                         data['description'])
        self.assertEqual(['application/json', 'text/html'],
                         data['renders'])
        parses = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']
        self.assertEqual(parses,
                         data['parses'])

    def test_02_list_no_args_kwargs(self):
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowListByYear.as_view()(request=request)
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

    def test_03_list_kwargs(self):
        kwargs = {'year': self.year}
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowListByYear.as_view()(request=request, **kwargs)
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

class TestCowDetailView(APITestCase):
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow']

    def setUp(self):
        client = Client.objects.get(pk=1)
        self.data = {'purchased_by': TestData.get_random_user(),
                     'purchase_date': TestTime.get_purchase_date(),
                     'age': TestData.get_age(),
                     'breed': 'Holstein',
                     'client': client.name,
                     'color': 'black_white'}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.herd = Cow.objects.all()
        self.pk = self.herd[0].id
        self.url = django_reverse('assets:cow-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.herd = None
        self.pk = None
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
        self.assertEquals(TestData.get_all_allowed_detail_methods(),
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

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
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
        self.assertGreaterEqual('2100-12-31',
                                data['sell_date'])
                             

class TestSeedListView(APITestCase):
    fixtures = ['client', 'cerealhay', 'grasshay', 'legumehay', 'pasture',
                'season', 'user', 'seed']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        client = Client.objects.get(pk=1)
        cereals = CerealHay.objects.all()
        cereal = cereals[randint(0, len(cereals) - 1)]
        grasses = GrassHay.objects.all()
        grass = grasses[randint(0, len(grasses) - 1)]
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        fields = Pasture.objects.all()
        pasture = fields[randint(0, len(fields) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.data = {'year': TestTime.get_year(),
                     'season': season.name,
                     'client': client.name,
                     'seeded_by': user.username,
                     'pasture': pasture.name,
                     'cereal_hay': cereal.name,
                     'grass_hay': grass.name,
                     'legume_hay': legume.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.url = django_reverse('assets:seed-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
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
        fields = Pasture.objects.all()
        self.assertLessEqual(1,
                             len(fields))
        seasons = Season.objects.all()
        self.assertLessEqual(4,
                             len(seasons))
        seeds = Seed.objects.all()
        self.assertLessEqual(10,
                             len(seeds))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = SeedList.as_view()(request=request)
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
        response = SeedList.as_view()(request=request)
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
            for key in TestData.get_seed_read_keys():
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
        response = SeedList.as_view()(request=request)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_seed_write_keys():
            self.assertIn(key,
                          data)

class TestSeedDetailView(APITestCase):
    fixtures = ['client', 'cerealhay', 'grasshay', 'legumehay', 'pasture',
                'season', 'user', 'seed']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        client = Client.objects.get(pk=1)
        cereals = CerealHay.objects.all()
        cereal = cereals[randint(0, len(cereals) - 1)]
        grasses = GrassHay.objects.all()
        grass = grasses[randint(0, len(grasses) - 1)]
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        fields = Pasture.objects.all()
        pasture = fields[randint(0, len(fields) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.data = {'year': TestTime.get_year(),
                     'season': season.name,
                     'client': client.name,
                     'seeded_by': user.username,
                     'pasture': pasture.name,
                     'cereal_hay': cereal.name,
                     'grass_hay': grass.name,
                     'legume_hay': legume.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.pk = Seed.objects.get(pk=1).id
        self.url = django_reverse('assets:seed-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
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
        fields = Pasture.objects.all()
        self.assertLessEqual(1,
                             len(fields))
        seasons = Season.objects.all()
        self.assertLessEqual(4,
                             len(seasons))
        seeds = Seed.objects.all()
        self.assertLessEqual(10,
                             len(seeds))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = SeedDetail.as_view()(request=request,
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
        response = SeedDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_seed_read_keys():
            self.assertIn(key,
                          data)

    def test_03_full_update(self):
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = SeedDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_seed_write_keys():
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
        response = SeedDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_seed_write_keys():
            self.assertIn(key,
                          data)

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = SeedDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

class TestEventListView(APITestCase):
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow',
                'action', 'event']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        actions = Action.objects.all()
        action = actions[randint(0, len(actions) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'client': cow.client.name,
                     'event_time': TestTime.get_datetime(),
                     'action': action.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.url = django_reverse('assets:event-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
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
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow',
                'action', 'event']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        actions = Action.objects.all()
        action = actions[randint(0, len(actions) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'client': cow.client.name,
                     'event_time': TestTime.get_datetime(),
                     'action': action.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.pk = Event.objects.get(pk=1).id
        self.url = django_reverse('assets:event-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
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
        self.assertEquals('GET, HEAD, OPTIONS',
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
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

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
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=self.pk)
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

class TestExerciseListView(APITestCase):
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow',
                'pasture', 'season', 'exercise']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        fields = Pasture.objects.all()
        pasture = fields[randint(0, len(fields) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'client': cow.client.name,
                     'exercise_time': TestTime.get_datetime(),
                     'pasture': pasture.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.url = django_reverse('assets:exercise-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
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
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow',
                'pasture', 'season', 'exercise']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        fields = Pasture.objects.all()
        pasture = fields[randint(0, len(fields) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'client': cow.client.name,
                     'exercise_time': TestTime.get_datetime(),
                     'pasture': pasture.name}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.pk = Exercise.objects.get(pk=1).id
        self.url = django_reverse('assets:exercise-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
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
        self.assertEquals('GET, HEAD, OPTIONS',
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
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

    def test_04_partial_update(self):
        data = {'pasture': self.data['pasture']}
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseDetail.as_view()(request=request,
                                            pk=self.pk)
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = ExerciseDetail.as_view()(request=request,
                                            pk=self.pk)
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

class TestMilkListView(APITestCase):
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow', 'milk']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        gallons = TestData.get_milk()
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'client': cow.client.name,
                     'milking_time': TestTime.get_datetime(),
                     'gallons': gallons}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.url = django_reverse('assets:milk-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
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
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow', 'milk']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        gallons = TestData.get_milk()
        self.data = {'recorded_by': user.username,
                     'cow': str(cow.rfid),
                     'client': cow.client.name,
                     'milking_time': TestTime.get_datetime(),
                     'gallons': gallons}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.pk = Milk.objects.get(pk=1).id
        self.url = django_reverse('assets:milk-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
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
        self.assertEquals('GET, HEAD, OPTIONS',
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
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

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
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

    def test_05_destroy(self):
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MilkDetail.as_view()(request=request,
                                        pk=self.pk)
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)

class TestHealthRecordListView(APITestCase):
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow', 'illness',
                'injury', 'status', 'treatment', 'vaccine', 'healthrecord']

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
                     'client': cow.client.name,
                     'inspection_time': TestTime.get_datetime(),
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
        self.url = django_reverse('assets:healthrecord-list')
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.herd = None
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
    fixtures = ['age', 'breed', 'client', 'color', 'user', 'cow', 'illness',
                'injury', 'status', 'treatment', 'vaccine', 'healthrecord']

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
                     'client': cow.client.name,
                     'inspection_time': TestTime.get_datetime(),
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
        self.pk = HealthRecord.objects.get(pk=1).id
        self.url = django_reverse('assets:healthrecord-detail',
                                  args=(self.pk,))
        self.user = User.objects.get(username=TestData.get_random_user())

    def tearDown(self):
        self.data = None
        self.factory = None
        self.pk = None
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
        self.assertEqual(405,
                         response.status_code)
        self.assertEqual('Method Not Allowed',
                         response.reason_phrase)
