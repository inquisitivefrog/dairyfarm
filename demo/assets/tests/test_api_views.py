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
from assets.api_views import ExerciseDetail, ExerciseList
from assets.models import Action, Age, Breed, BreedImage, Color, Cow, Event
from assets.models import Exercise, Pasture
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

class TestCowDetailView(APITestCase):
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
        pk = self.herd[0].id
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_detail_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_retrieve(self):
        pk = self.herd[0].id
        url = django_reverse('assets:cow-detail',
                             args=(pk,))
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=pk)
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
        self.assertIn('age',
                      data)
        self.assertIn('breed',
                      data)
        self.assertIn('color',
                      data)
        self.assertIn('image',
                      data)
        self.assertIn('link',
                      data)

    def test_03_full_update(self):
        pk = self.herd[0].id
        url = django_reverse('assets:cow-detail',
                             args=(pk,))
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=pk)
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
        self.assertEqual(self.data['image'],
                      data['image'])
        self.assertIn('link',
                      data)

    def test_04_partial_update(self):
        pk = self.herd[0].id
        data = {'age': self.data['age'],
                'breed': self.data['breed']}
        url = django_reverse('assets:cow-detail',
                             args=(pk,))
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=pk)
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
        self.assertIn('image',
                      data)
        self.assertIn('link',
                      data)

    def test_05_destroy(self):
        pk = self.herd[0].id
        url = django_reverse('assets:cow-detail',
                             args=(pk,))
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = CowDetail.as_view()(request=request,
                                       pk=pk)
        self.assertEqual(204,
                         response.status_code)
        self.assertEqual('No Content',
                         response.reason_phrase)

class TestEventListView(APITestCase):
    fixtures = ['age', 'breed', 'breedimage', 'color', 'user', 'cow',
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
        self.url = django_reverse('assets:cow-list')
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
        url = django_reverse('assets:event-list')
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
        url = django_reverse('assets:event-list')
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
    fixtures = ['age', 'breed', 'breedimage', 'color', 'user', 'cow',
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
        self.url = django_reverse('assets:cow-list')
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
        pk = Event.objects.get(pk=1).id
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=pk)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_detail_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_retrieve(self):
        pk = Event.objects.get(pk=1).id 
        url = django_reverse('assets:event-detail',
                             args=(pk,))
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=pk)
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
        self.assertIn('timestamp',
                      data)
        self.assertIn('recorded_by',
                      data)
        self.assertIn('cow',
                      data)
        self.assertIn('action',
                      data)
        self.assertIn('link',
                      data)

    def test_03_full_update(self):
        pk = Event.objects.get(pk=1).id 
        url = django_reverse('assets:event-detail',
                             args=(pk,))
        request = self.factory.put(path=self.url,
                                   data=dumps(self.data),
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=pk)
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
        pk = Event.objects.get(pk=1).id 
        data = {'action': self.data['action']}
        url = django_reverse('assets:event-detail',
                             args=(pk,))
        request = self.factory.patch(path=self.url,
                                     data=dumps(data),
                                     content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=pk)
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
        pk = Event.objects.get(pk=1).id 
        url = django_reverse('assets:event-detail',
                             args=(pk,))
        request = self.factory.delete(path=self.url,
                                      content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = EventDetail.as_view()(request=request,
                                         pk=pk)
        self.assertEqual(204,
                         response.status_code)
        self.assertEqual('No Content',
                         response.reason_phrase)

class TestExerciseListView(APITestCase):
    fixtures = ['age', 'breed', 'breedimage', 'color', 'user', 'cow',
                'cerealhay', 'grasshay', 'legumehay', 'region', 'regionimage',
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
        self.url = django_reverse('assets:cow-list')
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
        url = django_reverse('assets:exercise-list')
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
            for key in TestData.get_exercise_read_keys():
                self.assertIn(key,
                              event)

    def test_03_create(self):
        url = django_reverse('assets:exercise-list')
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

