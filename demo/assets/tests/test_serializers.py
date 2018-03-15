from random import randint

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from assets.models import Action, Age, Breed, BreedImage, Color, Cow, Event
from assets.models import CerealHay, GrassHay, LegumeHay, Pasture
from assets.models import Region, RegionImage, Season
from assets.serializers import CowSerializer, EventReadSerializer
from assets.serializers import EventWriteSerializer, ExerciseReadSerializer
from assets.serializers import ExerciseWriteSerializer
from assets.serializers import HealthRecordReadSerializer
from assets.serializers import HealthRecordWriteSerializer, MilkReadSerializer
from assets.serializers import MilkWriteSerializer, PastureSerializer
from assets.tests.utils import TestData, TestTime

class TestCowSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'breedimage', 'color', 'user', 'cow']

    def setUp(self):
        self._load_cow_data()
        self._load_model_data()

    def tearDown(self):
        self.cow_data = None
        self.model_data = None

    def _load_cow_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        ages = Age.objects.all()
        age = ages[randint(0, len(ages) - 1)]
        breeds = Breed.objects.all()
        breed = breeds[randint(0, len(breeds) - 1)]
        colors = Color.objects.all()
        color = colors[randint(0, len(colors) - 1)]
        images = BreedImage.objects.all()
        image = images[randint(0, len(images) - 1)]
        self.cow_data = {'purchased_by': user,
                         'purchase_date': TestTime.get_purchase_date(),
                         'age': age.name,
                         'breed': breed.name,
                         'color': color.name,
                         'image': image.url}

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        ages = Age.objects.all()
        age = ages[randint(0, len(ages) - 1)]
        breeds = Breed.objects.all()
        breed = breeds[randint(0, len(breeds) - 1)]
        colors = Color.objects.all()
        color = colors[randint(0, len(colors) - 1)]
        images = BreedImage.objects.all()
        image = images[randint(0, len(images) - 1)]
        self.model_data = {'purchased_by': user,
                           'purchase_date': TestTime.get_purchase_date(),
                           'age': age,
                           'breed': breed,
                           'color': color,
                           'image': image}

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        images = BreedImage.objects.all()
        self.assertEqual(7,
                         len(images))
        colors = Color.objects.all()
        self.assertEqual(9,
                         len(colors))
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))

    def test_01_create(self):
        actual = CowSerializer(data=self.cow_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('purchased_by',
                      actual.data)
        self.assertIn('purchase_date',
                      actual.data)
        self.assertIn('age',
                      actual.data)
        self.assertIn('breed',
                      actual.data)
        self.assertIn('color',
                      actual.data)
        self.assertIn('image',
                      actual.data)
        self.assertIn('link',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_cow_data()
            data.append(self.cow_data)
        actual = CowSerializer(data=data,
                               many=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('purchased_by',
                          actual.data[i])
            self.assertIn('purchase_date',
                          actual.data[i])
            self.assertIn('age',
                          actual.data[i])
            self.assertIn('breed',
                          actual.data[i])
            self.assertIn('color',
                          actual.data[i])
            self.assertIn('image',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

    def test_03_retrieve(self):
        cow = Cow.objects.get(id=1)
        actual = CowSerializer(cow)
        self.assertEqual(actual.data['purchased_by'],
                         TestData.get_random_user())
        self.assertRegex(actual.data['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['age'],
                         '\d year')
        self.assertRegex(actual.data['breed'],
                         '\w')
        self.assertRegex(actual.data['color'],
                         '\w_\w')
        self.assertRegex(actual.data['image'],
                         '/static/images/breeds/\w+.png')

    def test_04_list(self):
        expected = 10
        herd = []
        for i in range(expected):
            self._load_model_data()
            cow = Cow.objects.create(**self.model_data)
            herd.append(cow)
        actual = CowSerializer(herd,
                               many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('purchased_by',
                          actual.data[i])
            self.assertIn('purchase_date',
                          actual.data[i])
            self.assertIn('age',
                          actual.data[i])
            self.assertIn('breed',
                          actual.data[i])
            self.assertIn('color',
                          actual.data[i])
            self.assertIn('image',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

    def test_05_full_update(self):
        cow = Cow.objects.get(id=1)
        self._load_cow_data()
        actual = CowSerializer(cow,
                               data=self.cow_data,
                               partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.cow_data['purchased_by'].username,
                         actual.data['purchased_by'])
        self.assertEqual(self.cow_data['purchase_date'],
                         actual.data['purchase_date'])
        self.assertEqual(self.cow_data['age'],
                         actual.data['age'])
        self.assertEqual(self.cow_data['breed'],
                         actual.data['breed'])
        self.assertEqual(self.cow_data['color'],
                         actual.data['color'])
        self.assertEqual(self.cow_data['image'],
                         actual.data['image'])
        self.assertIn('link',
                      actual.data)

    def test_06_partial_update(self):
        cow = Cow.objects.get(id=1)
        self._load_cow_data()
        del self.cow_data['purchase_date']
        del self.cow_data['breed']
        del self.cow_data['image']
        actual = CowSerializer(cow,
                               data=self.cow_data,
                               partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.cow_data['purchased_by'].username,
                         actual.data['purchased_by'])
        self.assertEqual(self.cow_data['age'],
                         actual.data['age'])
        self.assertEqual(self.cow_data['color'],
                         actual.data['color'])
        self.assertIn('purchase_date',
                      actual.data)
        self.assertIn('breed',
                      actual.data)
        self.assertIn('image',
                      actual.data)
        self.assertIn('link',
                      actual.data)

class TestPastureSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['cerealhay', 'grasshay', 'legumehay', 'region', 'regionimage',
                'season', 'user', 'pasture']

    def setUp(self):
        self._load_pasture_data()
        self._load_model_data()

    def tearDown(self):
        self.pasture_data = None
        self.model_data = None

    def _load_pasture_data(self):
        fallow = False
        distance = TestData.get_distance()
        user = User.objects.get(username=TestData.get_random_user())
        cereals = CerealHay.objects.all()
        cereal = cereals[randint(0, len(cereals) - 1)]
        grasses = GrassHay.objects.all()
        grass = grasses[randint(0, len(grasses) - 1)]
        images = RegionImage.objects.all()
        image = images[randint(0, len(images) - 1)]
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        regions = Region.objects.all()
        region = regions[randint(0, len(regions) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.pasture_data = {'fallow': fallow,
                             'distance': distance,
                             'seeded_by': user,
                             'region': region.name,
                             'image': image.url,
                             'cereal_hay': cereal.name,
                             'grass_hay': grass.name,
                             'legume_hay': legume.name,
                             'season': season.name}

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        fallow = False
        distance = TestData.get_distance()
        user = User.objects.get(username=TestData.get_random_user())
        cereals = CerealHay.objects.all()
        cereal = cereals[randint(0, len(cereals) - 1)]
        grasses = GrassHay.objects.all()
        grass = grasses[randint(0, len(grasses) - 1)]
        images = RegionImage.objects.all()
        image = images[randint(0, len(images) - 1)]
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        regions = Region.objects.all()
        region = regions[randint(0, len(regions) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.model_data = {'fallow': fallow,
                           'distance': distance,
                           'seeded_by': user,
                           'region': region,
                           'image': image,
                           'cereal_hay': cereal,
                           'grass_hay': grass,
                           'legume_hay': legume,
                           'season': season}

    def test_00_load_fixtures(self):
        cereals = CerealHay.objects.all()
        self.assertEqual(5,
                         len(cereals))
        grasses = GrassHay.objects.all()
        self.assertEqual(9,
                         len(grasses))
        legumes = LegumeHay.objects.all()
        self.assertEqual(6,
                         len(legumes))
        pastures = Pasture.objects.all()
        self.assertEqual(13,
                         len(pastures))
        regions = Region.objects.all()
        self.assertEqual(13,
                         len(regions))
        images = RegionImage.objects.all()
        self.assertEqual(13,
                         len(images))
        seasons = Season.objects.all()
        self.assertEqual(4,
                         len(seasons))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))

    def test_01_create(self):
        actual = PastureSerializer(data=self.pasture_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('fallow',
                      actual.data)
        self.assertIn('distance',
                      actual.data)
        self.assertIn('seeded_by',
                      actual.data)
        self.assertIn('region',
                      actual.data)
        self.assertIn('image',
                      actual.data)
        self.assertIn('cereal_hay',
                      actual.data)
        self.assertIn('grass_hay',
                      actual.data)
        self.assertIn('legume_hay',
                      actual.data)
        self.assertIn('season',
                      actual.data)
        self.assertIn('link',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_pasture_data()
            data.append(self.pasture_data)
        actual = PastureSerializer(data=data,
                                   many=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('fallow',
                          actual.data[i])
            self.assertIn('distance',
                          actual.data[i])
            self.assertIn('seeded_by',
                          actual.data[i])
            self.assertIn('region',
                          actual.data[i])
            self.assertIn('image',
                          actual.data[i])
            self.assertIn('cereal_hay',
                          actual.data[i])
            self.assertIn('grass_hay',
                          actual.data[i])
            self.assertIn('legume_hay',
                          actual.data[i])
            self.assertIn('season',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

    def test_03_retrieve(self):
        pasture = Pasture.objects.get(id=1)
        actual = PastureSerializer(pasture)
        self.assertFalse(actual.data['fallow'])
        self.assertGreaterEqual(5,
                                actual.data['distance'])
        self.assertEqual(actual.data['seeded_by'],
                         TestData.get_random_user())
        self.assertRegex(actual.data['region'],
                         '^\w+$')
        self.assertRegex(actual.data['image'],
                         '^/static/images/regions/\w+')
        self.assertRegex(actual.data['cereal_hay'],
                         '^\w+$')
        self.assertRegex(actual.data['grass_hay'],
                         '^\w+$')
        self.assertRegex(actual.data['legume_hay'],
                         '^\w+$')
        self.assertRegex(actual.data['season'],
                         '^\w+$')

    def test_04_list(self):
        expected = 10
        fields = []
        for i in range(expected):
            self._load_model_data()
            pasture = Pasture.objects.create(**self.model_data)
            fields.append(pasture)
        actual = PastureSerializer(fields,
                               many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('fallow',
                          actual.data[i])
            self.assertIn('distance',
                          actual.data[i])
            self.assertIn('seeded_by',
                          actual.data[i])
            self.assertIn('region',
                          actual.data[i])
            self.assertIn('image',
                          actual.data[i])
            self.assertIn('cereal_hay',
                          actual.data[i])
            self.assertIn('grass_hay',
                          actual.data[i])
            self.assertIn('legume_hay',
                          actual.data[i])
            self.assertIn('season',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

    def test_05_full_update(self):
        pasture = Pasture.objects.get(id=1)
        self._load_pasture_data()
        actual = PastureSerializer(pasture,
                                   data=self.pasture_data,
                                   partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.pasture_data['fallow'],
                         actual.data['fallow'])
        self.assertEqual(self.pasture_data['distance'],
                         actual.data['distance'])
        self.assertEqual(self.pasture_data['seeded_by'].username,
                         actual.data['seeded_by'])
        self.assertEqual(self.pasture_data['region'],
                         actual.data['region'])
        self.assertEqual(self.pasture_data['image'],
                         actual.data['image'])
        self.assertEqual(self.pasture_data['cereal_hay'],
                         actual.data['cereal_hay'])
        self.assertEqual(self.pasture_data['grass_hay'],
                         actual.data['grass_hay'])
        self.assertEqual(self.pasture_data['legume_hay'],
                         actual.data['legume_hay'])
        self.assertEqual(self.pasture_data['season'],
                         actual.data['season'])

    def test_06_partial_update(self):
        pasture = Pasture.objects.get(id=1)
        self._load_pasture_data()
        del self.pasture_data['distance']
        del self.pasture_data['region']
        del self.pasture_data['season']
        actual = PastureSerializer(pasture,
                                   data=self.pasture_data,
                                   partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.pasture_data['fallow'],
                         actual.data['fallow'])
        self.assertEqual(pasture.distance,
                         actual.data['distance'])
        self.assertEqual(self.pasture_data['seeded_by'].username,
                         actual.data['seeded_by'])
        self.assertEqual(pasture.region.name,
                         actual.data['region'])
        self.assertEqual(self.pasture_data['image'],
                         actual.data['image'])
        self.assertEqual(self.pasture_data['cereal_hay'],
                         actual.data['cereal_hay'])
        self.assertEqual(self.pasture_data['grass_hay'],
                         actual.data['grass_hay'])
        self.assertEqual(self.pasture_data['legume_hay'],
                         actual.data['legume_hay'])
        self.assertEqual(pasture.season.name,
                         actual.data['season'])

class TestEventReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'breedimage', 'color', 'user', 'cow', 'action', 'event']

    def setUp(self):
        self._load_model_data()

    def tearDown(self):
        self.model_data = None

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        actions = Action.objects.all()
        action = actions[randint(0, len(actions) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.model_data = {'recorded_by': user,
                           'cow': cow,
                           'action': action}

    def test_00_load_fixtures(self):
        actions = Action.objects.all()
        self.assertEqual(17,
                         len(actions))
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        events = Event.objects.all()
        self.assertEqual(134,
                         len(events))

    def test_01_retrieve(self):
        event = Event.objects.get(pk=1)
        actual = EventReadSerializer(event)
        self.assertGreaterEqual(10,
                                actual.data['id'])
        self.assertRegex(actual.data['recorded_by'],
                         '\w')
        self.assertRegex(actual.data['timestamp'],
                         '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$')
        self.assertGreaterEqual(10,
                                actual.data['cow']['id'])
        self.assertRegex(actual.data['cow']['rfid'],
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertRegex(actual.data['cow']['purchased_by'],
                         '\w')
        self.assertRegex(actual.data['cow']['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['cow']['age'],
                         '\d years')
        self.assertRegex(actual.data['cow']['breed'],
                         '\w')
        self.assertRegex(actual.data['cow']['color'],
                         '\w_\w')
        self.assertRegex(actual.data['cow']['image'],
                         '/static/images/breeds/\w+\.png')
        self.assertRegex(actual.data['cow']['link'],
                         '/assets/api/cows/\d/')
        self.assertRegex(actual.data['action'],
                         '\w+')
        self.assertRegex(actual.data['link'],
                         '/assets/api/events/\d/')

    def test_02_list(self):
        expected = 10
        events = []
        for i in range(expected):
            self._load_model_data()
            event = Event.objects.create(**self.model_data)
            events.append(event)
        actual = EventReadSerializer(events,
                                     many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('timestamp',
                          actual.data[i])
            self.assertIn('id',
                          actual.data[i]['cow'])
            self.assertIn('rfid',
                          actual.data[i]['cow'])
            self.assertIn('purchased_by',
                          actual.data[i]['cow'])
            self.assertIn('purchase_date',
                          actual.data[i]['cow'])
            self.assertIn('breed',
                          actual.data[i]['cow'])
            self.assertIn('color',
                          actual.data[i]['cow'])
            self.assertIn('image',
                          actual.data[i]['cow'])
            self.assertIn('link',
                          actual.data[i]['cow'])
            self.assertIn('action',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestEventWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'breedimage', 'color', 'user', 'cow', 'action', 'event']

    def setUp(self):
        self._load_event_data()

    def tearDown(self):
        self.event_data = None

    def _load_event_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        actions = Action.objects.all()
        action = actions[randint(0, len(actions) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.event_data = {'recorded_by': user,
                           'cow': cow.rfid,
                           'action': action.name}

    def test_00_load_fixtures(self):
        actions = Action.objects.all()
        self.assertEqual(17,
                         len(actions))
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        events = Event.objects.all()
        self.assertEqual(134,
                         len(events))

    def test_01_create(self):
        actual = EventWriteSerializer(data=self.event_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('recorded_by',
                      actual.data)
        self.assertIn('cow',
                      actual.data)
        self.assertIn('action',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_event_data()
            data.append(self.event_data)
        actual = EventWriteSerializer(data=data,
                                      many=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('cow',
                          actual.data[i])
            self.assertIn('action',
                          actual.data[i])

    def test_03_full_update(self):
        event = Event.objects.get(id=1)
        self._load_event_data()
        self.event_data.update({'cow': event.cow.rfid})
        actual = EventWriteSerializer(event,
                                      data=self.event_data,
                                      partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.event_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.event_data['cow'],
                         actual.data['cow'])
        self.assertEqual(self.event_data['action'],
                         actual.data['action'])

    def test_04_partial_update(self):
        event = Event.objects.get(id=1)
        self._load_event_data()
        self.event_data.update({'cow': event.cow.rfid})
        del self.event_data['action']
        actual = EventWriteSerializer(event,
                                      data=self.event_data,
                                      partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.event_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.event_data['cow'],
                         actual.data['cow'])
        self.assertEqual(event.action.name,
                         actual.data['action'])
