from random import randint

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from assets.models import Action, Age, Breed, CerealHay, Client, Color, Cow
from assets.models import Event, Exercise, GrassHay, HealthRecord, Illness
from assets.models import Injury, LegumeHay, Milk, Pasture, Season
from assets.models import Seed, Status, Treatment, Vaccine
from assets.serializers import ActionSerializer, AgeSerializer
from assets.serializers import BreedSerializer, ColorSerializer, ClientSerializer
from assets.serializers import CerealHaySerializer, GrassHaySerializer
from assets.serializers import IllnessSerializer, InjurySerializer
from assets.serializers import LegumeHaySerializer
from assets.serializers import SeasonSerializer, StatusSerializer
from assets.serializers import TreatmentSerializer, VaccineSerializer
from assets.serializers import CowReadSerializer, CowWriteSerializer
from assets.serializers import EventReadSerializer, EventWriteSerializer
from assets.serializers import ExerciseReadSerializer, ExerciseWriteSerializer
from assets.serializers import HealthRecordReadSerializer, HealthRecordWriteSerializer
from assets.serializers import MilkReadSerializer, MilkWriteSerializer
from assets.serializers import PastureReadSerializer, PastureWriteSerializer
from assets.serializers import SeedReadSerializer, SeedWriteSerializer
from assets.tests.utils import TestData, TestTime

class TestActionSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['action']

    def setUp(self):
        self._load_action_data()

    def tearDown(self):
        self.action_data = None

    def _load_action_data(self):
        self.action_data = {'name': TestData.get_action()}

    def test_00_load_fixtures(self):
        actions = Action.objects.all()
        self.assertLessEqual(17,
                             len(actions))

    def test_01_create(self):
        actual = ActionSerializer(data=self.action_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_action_data()
            self.action_data.update({'name': '{} {}'.format(self.action_data['name'], i)})
            data.append(self.action_data)
        actual = ActionSerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        action = Action.objects.get(id=1)
        actual = ActionSerializer(action)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        actions = []
        for i in range(expected):
            self._load_action_data()
            self.action_data.update({'name': '{} {}'.format(self.action_data['name'], i)})
            action = Action.objects.create(**self.action_data)
            actions.append(action)
        actual = ActionSerializer(actions,
                                  many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        action = Action.objects.get(id=1)
        self._load_action_data()
        self.action_data.update({'name': TestData.get_action()})
        actual = ActionSerializer(action,
                                  data=self.action_data,
                                  partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.action_data['name'],
                         actual.data['name'])

class TestAgeSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age']

    def setUp(self):
        self._load_age_data()

    def tearDown(self):
        self.age_data = None

    def _load_age_data(self):
        self.age_data = {'name': '{} years'.format(randint(10, 10000))}

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertLessEqual(5,
                             len(ages))

    def test_01_create(self):
        actual = AgeSerializer(data=self.age_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_age_data()
            data.append(self.age_data)
        actual = AgeSerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        age = Age.objects.get(id=1)
        actual = AgeSerializer(age)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        ages = []
        for i in range(expected):
            self._load_age_data()
            age = Age.objects.create(**self.age_data)
            ages.append(age)
        actual = AgeSerializer(ages,
                               many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        age = Age.objects.get(id=1)
        self._load_age_data()
        actual = AgeSerializer(age,
                               data=self.age_data,
                               partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.age_data['name'],
                         actual.data['name'])

class TestBreedSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['breed']

    def setUp(self):
        self._load_breed_data()

    def tearDown(self):
        self.breed_data = None

    def _load_breed_data(self):
        name = '{}_{}'.format(TestData.get_breed(), randint(10, 10000))
        self.breed_data = {'name': name,
                           'url': '/static/images/breeds/{}.jpg'.format(name.lower())}

    def test_00_load_fixtures(self):
        breeds = Breed.objects.all()
        self.assertLessEqual(7,
                             len(breeds))

    def test_01_create(self):
        actual = BreedSerializer(data=self.breed_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_breed_data()
            data.append(self.breed_data)
        actual = BreedSerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        breed = Breed.objects.get(id=1)
        actual = BreedSerializer(breed)
        self.assertRegex(actual.data['name'],
                         '\w+')
        self.assertRegex(actual.data['url'],
                         '/static/images/breeds/\w+\.png')

    def test_04_list(self):
        expected = 10
        breeds = []
        for i in range(expected):
            self._load_breed_data()
            breed = Breed.objects.create(**self.breed_data)
            breeds.append(breed)
        actual = BreedSerializer(breeds,
                                 many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])
            self.assertIn('url',
                          actual.data[i])

    def test_05_full_update(self):
        breed = Breed.objects.get(id=1)
        self._load_breed_data()
        actual = BreedSerializer(breed,
                                 data=self.breed_data,
                                 partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.breed_data['name'],
                         actual.data['name'])
        self.assertEqual(self.breed_data['url'],
                         actual.data['url'])

    def test_06_partial_update(self):
        breed = Breed.objects.get(id=1)
        self._load_breed_data()
        del self.breed_data['url']
        actual = BreedSerializer(breed,
                                 data=self.breed_data,
                                 partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.breed_data['name'],
                         actual.data['name'])
        self.assertEqual(breed.url,
                         actual.data['url'])

class TestClientSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['user', 'client']

    def setUp(self):
        self._load_client_data()

    def tearDown(self):
        self.client_data = None

    def _load_client_data(self):
        username = TestData.get_random_user()
        user = User.objects.get(username=username)
        self.client_data = {'user': TestData.get_random_user(),
                            'name': TestData.get_random_client(),
                            'join_date': TestTime.get_date()}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))

    def test_01_create(self):
        actual = ClientSerializer(data=self.client_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)
        self.assertRegex(actual.data['join_date'],
                         '^\d{4}-\d{2}-\d{2}')
        self.assertRegex(actual.data['inactive_date'],
                         '^\d{4}-\d{2}-\d{2}')

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_client_data()
            self.client_data.update({'name': '{} {}'.format(self.client_data['name'], i)})
            data.append(self.client_data)
        actual = ClientSerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])
            self.assertIn('join_date',
                          actual.data[i])
            self.assertIn('inactive_date',
                          actual.data[i])

    def test_03_retrieve(self):
        client = Client.objects.get(id=1)
        actual = ClientSerializer(client)
        self.assertRegex(actual.data['name'],
                         '\w+')
        self.assertRegex(actual.data['join_date'],
                         '^\d{4}-\d{2}-\d{2}')
        self.assertRegex(actual.data['inactive_date'],
                         '^\d{4}-\d{2}-\d{2}')

    def test_04_list(self):
        expected = 10
        clients = []
        for i in range(expected):
            self._load_client_data()
            self.client_data.update({'name': '{} {}'.format(self.client_data['name'], i)})
            self.client_data.update({'user': User.objects.get(username=self.client_data['user'])})
            client = Client.objects.create(**self.client_data)
            clients.append(client)
        actual = ClientSerializer(clients,
                                  many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])
            self.assertIn('join_date',
                          actual.data[i])
            self.assertIn('inactive_date',
                          actual.data[i])

    def test_05_full_update(self):
        client = Client.objects.get(id=1)
        self._load_client_data()
        actual = ClientSerializer(client,
                                  data=self.client_data,
                                  partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.client_data['name'],
                         actual.data['name'])
        self.assertEqual(TestTime.convert_date(self.client_data['join_date']),
                         actual.data['join_date'])
        self.assertEqual(TestTime.convert_date(client.inactive_date),
                         actual.data['inactive_date'])

class TestCerealHaySerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['cerealhay']

    def setUp(self):
        self._load_cereal_data()

    def tearDown(self):
        self.cereal_data = None

    def _load_cereal_data(self):
        name = '{}_{}'.format(TestData.get_cereal(), randint(10, 10000))
        self.cereal_data = {'name': name}

    def test_00_load_fixtures(self):
        cereals = CerealHay.objects.all()
        self.assertLessEqual(5,
                             len(cereals))

    def test_01_create(self):
        actual = CerealHaySerializer(data=self.cereal_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_cereal_data()
            data.append(self.cereal_data)
        actual = CerealHaySerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        cereal = CerealHay.objects.get(id=1)
        actual = CerealHaySerializer(cereal)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        cereals = []
        for i in range(expected):
            self._load_cereal_data()
            cereal = CerealHay.objects.create(**self.cereal_data)
            cereals.append(cereal)
        actual = CerealHaySerializer(cereals,
                                     many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        cereal = CerealHay.objects.get(id=1)
        self._load_cereal_data()
        actual = CerealHaySerializer(cereal,
                                     data=self.cereal_data,
                                     partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.cereal_data['name'],
                         actual.data['name'])

class TestGrassHaySerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['grasshay']

    def setUp(self):
        self._load_grass_data()

    def tearDown(self):
        self.grass_data = None

    def _load_grass_data(self):
        name = '{}_{}'.format(TestData.get_grass(), randint(10, 10000))
        self.grass_data = {'name': name}

    def test_00_load_fixtures(self):
        grasses = GrassHay.objects.all()
        self.assertLessEqual(9,
                             len(grasses))

    def test_01_create(self):
        actual = GrassHaySerializer(data=self.grass_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_grass_data()
            data.append(self.grass_data)
        actual = GrassHaySerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        grass = GrassHay.objects.get(id=1)
        actual = GrassHaySerializer(grass)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        grasses = []
        for i in range(expected):
            self._load_grass_data()
            grass = GrassHay.objects.create(**self.grass_data)
            grasses.append(grass)
        actual = GrassHaySerializer(grasses,
                                     many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        grass = GrassHay.objects.get(id=1)
        self._load_grass_data()
        actual = GrassHaySerializer(grass,
                                     data=self.grass_data,
                                     partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.grass_data['name'],
                         actual.data['name'])

class TestIllnessSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['illness']

    def setUp(self):
        self._load_illness_data()

    def tearDown(self):
        self.illness_data = None

    def _load_illness_data(self):
        diagnosis = '{}_{}'.format(TestData.get_illness(), randint(10, 10000))
        treatment = '{}_{}'.format(TestData.get_treatment(), randint(10, 10000))
        self.illness_data = {'diagnosis': diagnosis,
                             'treatment': treatment}

    def test_00_load_fixtures(self):
        illnesses = Illness.objects.all()
        self.assertLessEqual(15,
                             len(illnesses))

    def test_01_create(self):
        actual = IllnessSerializer(data=self.illness_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('diagnosis',
                      actual.data)
        self.assertIn('treatment',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_illness_data()
            data.append(self.illness_data)
        actual = IllnessSerializer(data=data,
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
            self.assertIn('diagnosis',
                          actual.data[i])
            self.assertIn('treatment',
                          actual.data[i])

    def test_03_retrieve(self):
        illness = Illness.objects.get(id=1)
        actual = IllnessSerializer(illness)
        self.assertRegex(actual.data['diagnosis'],
                         '\w+')
        self.assertRegex(actual.data['treatment'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        illnesses = []
        for i in range(expected):
            self._load_illness_data()
            illness = Illness.objects.create(**self.illness_data)
            illnesses.append(illness)
        actual = IllnessSerializer(illnesses,
                                   many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('diagnosis',
                          actual.data[i])
            self.assertIn('treatment',
                          actual.data[i])

    def test_05_full_update(self):
        illness = Illness.objects.get(id=1)
        self._load_illness_data()
        actual = IllnessSerializer(illness,
                                 data=self.illness_data,
                                 partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.illness_data['diagnosis'],
                         actual.data['diagnosis'])
        self.assertEqual(self.illness_data['treatment'],
                         actual.data['treatment'])

    def test_06_partial_update(self):
        illness = Illness.objects.get(id=1)
        self._load_illness_data()
        del self.illness_data['treatment']
        actual = IllnessSerializer(illness,
                                   data=self.illness_data,
                                   partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.illness_data['diagnosis'],
                         actual.data['diagnosis'])
        self.assertEqual(illness.treatment,
                         actual.data['treatment'])

class TestInjurySerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['injury']

    def setUp(self):
        self._load_injury_data()

    def tearDown(self):
        self.injury_data = None

    def _load_injury_data(self):
        diagnosis = '{}_{}'.format(TestData.get_injury(), randint(10, 10000))
        treatment = '{}_{}'.format(TestData.get_treatment(), randint(10, 10000))
        self.injury_data = {'diagnosis': diagnosis,
                            'treatment': treatment}

    def test_00_load_fixtures(self):
        injuries = Injury.objects.all()
        self.assertLessEqual(5,
                             len(injuries))

    def test_01_create(self):
        actual = InjurySerializer(data=self.injury_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('diagnosis',
                      actual.data)
        self.assertIn('treatment',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_injury_data()
            data.append(self.injury_data)
        actual = InjurySerializer(data=data,
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
            self.assertIn('diagnosis',
                          actual.data[i])
            self.assertIn('treatment',
                          actual.data[i])

    def test_03_retrieve(self):
        injury = Injury.objects.get(id=1)
        actual = InjurySerializer(injury)
        self.assertRegex(actual.data['diagnosis'],
                         '\w+')
        self.assertRegex(actual.data['treatment'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        injuries = []
        for i in range(expected):
            self._load_injury_data()
            injury = Injury.objects.create(**self.injury_data)
            injuries.append(injury)
        actual = InjurySerializer(injuries,
                                  many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('diagnosis',
                          actual.data[i])
            self.assertIn('treatment',
                          actual.data[i])

    def test_05_full_update(self):
        injury = Injury.objects.get(id=1)
        self._load_injury_data()
        actual = InjurySerializer(injury,
                                  data=self.injury_data,
                                  partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.injury_data['diagnosis'],
                         actual.data['diagnosis'])
        self.assertEqual(self.injury_data['treatment'],
                         actual.data['treatment'])

    def test_06_partial_update(self):
        injury = Injury.objects.get(id=1)
        self._load_injury_data()
        del self.injury_data['treatment']
        actual = InjurySerializer(injury,
                                  data=self.injury_data,
                                  partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.injury_data['diagnosis'],
                         actual.data['diagnosis'])
        self.assertEqual(injury.treatment,
                         actual.data['treatment'])

class TestLegumeHaySerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['legumehay']

    def setUp(self):
        self._load_legume_data()

    def tearDown(self):
        self.legume_data = None

    def _load_legume_data(self):
        name = '{}_{}'.format(TestData.get_legume(), randint(10, 10000))
        self.legume_data = {'name': name}

    def test_00_load_fixtures(self):
        legumes = LegumeHay.objects.all()
        self.assertLessEqual(6,
                             len(legumes))

    def test_01_create(self):
        actual = LegumeHaySerializer(data=self.legume_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_legume_data()
            data.append(self.legume_data)
        actual = LegumeHaySerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        legume = LegumeHay.objects.get(id=1)
        actual = LegumeHaySerializer(legume)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        legumes = []
        for i in range(expected):
            self._load_legume_data()
            legume = LegumeHay.objects.create(**self.legume_data)
            legumes.append(legume)
        actual = LegumeHaySerializer(legumes,
                                     many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        legume = LegumeHay.objects.get(id=1)
        self._load_legume_data()
        actual = LegumeHaySerializer(legume,
                                     data=self.legume_data,
                                     partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.legume_data['name'],
                         actual.data['name'])

class TestPastureReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['user', 'client', 'pasture']

    def setUp(self):
        self._load_pasture_data()

    def tearDown(self):
        self.pasture_data = None

    def _load_pasture_data(self):
        client = Client.objects.get(pk=1)
        pasture = Pasture.objects.get(pk=1)
        self.pasture_data = {'client': client,
                             'name': pasture.name,
                             'url': pasture.url,
                             'fallow': False,
                             'distance': randint(1, 12)}

    def test_00_load_fixtures(self):
        users = User.objects.all()
        self.assertLessEqual(5,
                             len(users))
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        fields = Pasture.objects.all()
        self.assertLessEqual(13,
                             len(fields))

    def test_01_retrieve(self):
        pasture = Pasture.objects.get(id=1)
        actual = PastureReadSerializer(pasture)
        self.assertRegex(actual.data['client']['name'],
                         '\w+')
        self.assertRegex(actual.data['name'],
                         '\w+')
        self.assertRegex(actual.data['url'],
                         '/static/images/regions/\w+\.jpg$')
        self.assertIsInstance(actual.data['fallow'],
                              bool)
        self.assertLessEqual(1,
                             actual.data['distance'])

    def test_02_list(self):
        expected = 10
        fields = []
        for i in range(expected):
            self._load_pasture_data()
            self.pasture_data.update({'name': '{} {}'.format(self.pasture_data['name'], i),
                                      'url': '{}_{}.png'.format(self.pasture_data['url'][0:-4], i)})
            pasture= Pasture.objects.create(**self.pasture_data)
            fields.append(pasture)
        actual = PastureReadSerializer(fields,
                                       many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])
            self.assertIn('url',
                          actual.data[i])
            self.assertIn('fallow',
                          actual.data[i])
            self.assertIn('distance',
                          actual.data[i])

class TestPastureWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['user', 'client', 'pasture']

    def setUp(self):
        self._load_pasture_data()

    def tearDown(self):
        self.pasture_data = None

    def _load_pasture_data(self):
        client = Client.objects.get(pk=1)
        name = '{}_{}'.format(TestData.get_pasture(), randint(10, 10000))
        url = '/static/images/regions/{}.png'.format(name.lower())
        self.pasture_data = {'client': client,
                             'name': name,
                             'url': url,
                             'fallow': False,
                             'distance': randint(1, 12)}

    def test_00_load_fixtures(self):
        users = User.objects.all()
        self.assertLessEqual(5,
                             len(users))
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        fields = Pasture.objects.all()
        self.assertLessEqual(13,
                             len(fields))

    def test_01_create(self):
        actual = PastureWriteSerializer(data=self.pasture_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('client',
                      actual.data)
        self.assertIn('name',
                      actual.data)
        self.assertIn('url',
                      actual.data)
        self.assertIn('fallow',
                      actual.data)
        self.assertIn('distance',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_pasture_data()
            self.pasture_data.update({'name': '{}_{}'.format(self.pasture_data['name'], i)})
            self.pasture_data.update({'url': '{}_{}'.format(self.pasture_data['url'], i)})
            data.append(self.pasture_data)
        actual = PastureWriteSerializer(data=data,
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
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])
            self.assertIn('url',
                          actual.data[i])
            self.assertIn('fallow',
                          actual.data[i])
            self.assertIn('distance',
                          actual.data[i])

    def test_03_full_update(self):
        pasture = Pasture.objects.get(id=1)
        self._load_pasture_data()
        actual = PastureWriteSerializer(pasture,
                                        data=self.pasture_data,
                                        partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.pasture_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.pasture_data['name'],
                         actual.data['name'])
        self.assertEqual(self.pasture_data['url'],
                         actual.data['url'])
        self.assertEqual(self.pasture_data['fallow'],
                         actual.data['fallow'])
        self.assertEqual(self.pasture_data['distance'],
                         actual.data['distance'])

    def test_04_partial_update(self):
        pasture = Pasture.objects.get(id=1)
        self._load_pasture_data()
        del self.pasture_data['fallow']
        del self.pasture_data['distance']
        actual = PastureWriteSerializer(pasture,
                                        data=self.pasture_data,
                                        partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.pasture_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.pasture_data['name'],
                         actual.data['name'])
        self.assertEqual(self.pasture_data['url'],
                         actual.data['url'])
        self.assertIn('fallow',
                      actual.data)
        self.assertIn('distance',
                      actual.data)

class TestSeasonSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['season']

    def setUp(self):
        self._load_season_data()

    def tearDown(self):
        self.season_data = None

    def _load_season_data(self):
        name = '{}_{}'.format(TestData.get_season(), randint(10, 10000))
        self.season_data = {'name': name}

    def test_00_load_fixtures(self):
        seasons = Season.objects.all()
        self.assertLessEqual(4,
                             len(seasons))

    def test_01_create(self):
        actual = SeasonSerializer(data=self.season_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_season_data()
            self.season_data.update({'name': '{} {}'.format(self.season_data['name'], i)})
            data.append(self.season_data)
        actual = SeasonSerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        season = Season.objects.get(id=1)
        actual = SeasonSerializer(season)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        seasons = []
        for i in range(expected):
            self._load_season_data()
            self.season_data.update({'name': '{} {}'.format(self.season_data['name'], i)})
            season = Season.objects.create(**self.season_data)
            seasons.append(season)
        actual = SeasonSerializer(seasons,
                                  many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        season = Season.objects.get(id=1)
        self._load_season_data()
        actual = SeasonSerializer(season,
                                  data=self.season_data,
                                  partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.season_data['name'],
                         actual.data['name'])

class TestStatusSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['status']

    def setUp(self):
        self._load_status_data()

    def tearDown(self):
        self.status_data = None

    def _load_status_data(self):
        name = '{}_{}'.format(TestData.get_status(), randint(10, 10000))
        self.status_data = {'name': name}

    def test_00_load_fixtures(self):
        statuses = Status.objects.all()
        self.assertEqual(5,
                         len(statuses))

    def test_01_create(self):
        actual = StatusSerializer(data=self.status_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_status_data()
            self.status_data.update({'name': '{} {}'.format(self.status_data['name'], i)})
            data.append(self.status_data)
        actual = StatusSerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        status = Status.objects.get(id=1)
        actual = StatusSerializer(status)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        statuses = []
        for i in range(expected):
            self._load_status_data()
            self.status_data.update({'name': '{} {}'.format(self.status_data['name'], i)})
            status = Status.objects.create(**self.status_data)
            statuses.append(status)
        actual = StatusSerializer(statuses,
                                  many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        status = Status.objects.get(id=1)
        self._load_status_data()
        actual = StatusSerializer(status,
                                  data=self.status_data,
                                  partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.status_data['name'],
                         actual.data['name'])

class TestTreatmentSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['treatment']

    def setUp(self):
        self._load_treatment_data()

    def tearDown(self):
        self.treatment_data = None

    def _load_treatment_data(self):
        name = '{}_{}'.format('apply_salve', randint(10, 10000))
        self.treatment_data = {'name': name}

    def test_00_load_fixtures(self):
        treatments = Treatment.objects.all()
        self.assertEqual(14,
                         len(treatments))

    def test_01_create(self):
        actual = TreatmentSerializer(data=self.treatment_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_treatment_data()
            data.append(self.treatment_data)
        actual = TreatmentSerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        treatment = Treatment.objects.get(id=1)
        actual = TreatmentSerializer(treatment)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        treatments = []
        for i in range(expected):
            self._load_treatment_data()
            treatment = Treatment.objects.create(**self.treatment_data)
            treatments.append(treatment)
        actual = TreatmentSerializer(treatments,
                                  many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        treatment = Treatment.objects.get(id=1)
        self._load_treatment_data()
        actual = TreatmentSerializer(treatment,
                                  data=self.treatment_data,
                                  partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.treatment_data['name'],
                         actual.data['name'])

class TestVaccineSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['vaccine']

    def setUp(self):
        self._load_vaccine_data()

    def tearDown(self):
        self.vaccine_data = None

    def _load_vaccine_data(self):
        name = '{}_{}'.format('take vaccine', randint(10, 10000))
        self.vaccine_data = {'name': name}

    def test_00_load_fixtures(self):
        vaccines = Vaccine.objects.all()
        self.assertEqual(6,
                         len(vaccines))

    def test_01_create(self):
        actual = VaccineSerializer(data=self.vaccine_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_vaccine_data()
            data.append(self.vaccine_data)
        actual = VaccineSerializer(data=data,
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
            self.assertIn('name',
                          actual.data[i])

    def test_03_retrieve(self):
        vaccine = Vaccine.objects.get(id=1)
        actual = VaccineSerializer(vaccine)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        vaccines = []
        for i in range(expected):
            self._load_vaccine_data()
            vaccine = Vaccine.objects.create(**self.vaccine_data)
            vaccines.append(vaccine)
        actual = VaccineSerializer(vaccines,
                                   many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        vaccine = Vaccine.objects.get(id=1)
        self._load_vaccine_data()
        actual = VaccineSerializer(vaccine,
                                  data=self.vaccine_data,
                                  partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.vaccine_data['name'],
                         actual.data['name'])

class TestCowReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow']

    def setUp(self):
        self._load_model_data()

    def tearDown(self):
        self.model_data = None

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        ages = Age.objects.all()
        age = ages[randint(0, len(ages) - 1)]
        breeds = Breed.objects.all()
        breed = breeds[randint(0, len(breeds) - 1)]
        clients = Client.objects.all()
        client = clients[randint(0, len(clients) - 1)]
        colors = Color.objects.all()
        color = colors[randint(0, len(colors) - 1)]
        self.model_data = {'purchased_by': user,
                           'purchase_date': TestTime.get_date(),
                           'age': age,
                           'breed': breed,
                           'client': client,
                           'color': color,
                           'sell_date': '2018-12-31'}

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertLessEqual(5,
                             len(ages))
        breeds = Breed.objects.all()
        self.assertLessEqual(7,
                             len(breeds))
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        colors = Color.objects.all()
        self.assertLessEqual(9,
                             len(colors))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))

    def test_01_retrieve(self):
        cow = Cow.objects.get(id=1)
        actual = CowReadSerializer(cow)
        self.assertEqual(actual.data['purchased_by'],
                         TestData.get_random_user())
        self.assertRegex(actual.data['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['age']['name'],
                         '\d year')
        self.assertRegex(actual.data['breed']['name'],
                         '\w')
        self.assertRegex(actual.data['color']['name'],
                         '\w_\w')
        self.assertRegex(actual.data['client']['name'],
                         '^\w')

    def test_02_list(self):
        expected = 10
        herd = []
        for i in range(expected):
            self._load_model_data()
            cow = Cow.objects.create(**self.model_data)
            herd.append(cow)
        actual = CowReadSerializer(herd,
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
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('color',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestCowWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow']

    def setUp(self):
        self._load_cow_data()

    def tearDown(self):
        self.cow_data = None

    def _load_cow_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        ages = Age.objects.all()
        age = ages[randint(0, len(ages) - 1)]
        breeds = Breed.objects.all()
        breed = breeds[randint(0, len(breeds) - 1)]
        clients = Client.objects.all()
        client = clients[randint(0, len(clients) - 1)]
        colors = Color.objects.all()
        color = colors[randint(0, len(colors) - 1)]
        self.cow_data = {'purchased_by': user,
                         'purchase_date': TestTime.get_date(),
                         'age': age.name,
                         'breed': breed.name,
                         'client': client,
                         'color': color.name,
                         'sell_date': '2018-12-31'}

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertLessEqual(5,
                             len(ages))
        breeds = Breed.objects.all()
        self.assertLessEqual(7,
                             len(breeds))
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        colors = Color.objects.all()
        self.assertLessEqual(9,
                             len(colors))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))

    def test_01_create(self):
        actual = CowWriteSerializer(data=self.cow_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('rfid',
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
        self.assertIn('client',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_cow_data()
            data.append(self.cow_data)
        actual = CowWriteSerializer(data=data,
                               many=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('rfid',
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
            self.assertIn('client',
                          actual.data[i])

    def test_03_full_update(self):
        cow = Cow.objects.get(id=1)
        self._load_cow_data()
        actual = CowWriteSerializer(cow,
                                    data=self.cow_data,
                                    partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.cow_data['purchased_by'].username,
                         actual.data['purchased_by'])
        self.assertEqual(TestTime.convert_date(self.cow_data['purchase_date']),
                         actual.data['purchase_date'])
        self.assertEqual(self.cow_data['age'],
                         actual.data['age'])
        self.assertEqual(self.cow_data['breed'],
                         actual.data['breed'])
        self.assertEqual(self.cow_data['color'],
                         actual.data['color'])
        self.assertEqual(self.cow_data['client'].name,
                         actual.data['client'])

    def test_04_partial_update(self):
        cow = Cow.objects.get(id=1)
        self._load_cow_data()
        del self.cow_data['purchase_date']
        del self.cow_data['breed']
        actual = CowWriteSerializer(cow,
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
        self.assertEqual(self.cow_data['client'].name,
                         actual.data['client'])
        self.assertIn('purchase_date',
                      actual.data)
        self.assertIn('breed',
                      actual.data)

class TestEventReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow', 'action', 'event']

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
                           'client': cow.client,
                           'event_time': TestTime.get_datetime(),
                           'action': action}

    def test_00_load_fixtures(self):
        actions = Action.objects.all()
        self.assertLessEqual(17,
                             len(actions))
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        events = Event.objects.all()
        self.assertLessEqual(10,
                             len(events))

    def test_01_retrieve(self):
        event = Event.objects.get(pk=1)
        actual = EventReadSerializer(event)
        self.assertGreaterEqual(10,
                                actual.data['id'])
        self.assertRegex(actual.data['recorded_by'],
                         '\w')
        self.assertRegex(actual.data['event_time'],
                         '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}$')
        self.assertGreaterEqual(10,
                                actual.data['cow']['id'])
        self.assertRegex(actual.data['cow']['rfid'],
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertRegex(actual.data['cow']['purchased_by'],
                         '\w')
        self.assertRegex(actual.data['cow']['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['cow']['age']['name'],
                         '\d year')
        self.assertRegex(actual.data['cow']['breed']['name'],
                         '\w')
        self.assertRegex(actual.data['cow']['color']['name'],
                         '\w_\w')
        self.assertRegex(actual.data['cow']['link'],
                         '/assets/api/cows/\d/')
        self.assertRegex(actual.data['client']['name'],
                         '\w+')
        self.assertRegex(actual.data['action']['name'],
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
            self.assertIn('event_time',
                          actual.data[i])
            self.assertIn('id',
                          actual.data[i]['cow'])
            #self.assertIn('rfid',
            #              actual.data[i]['cow'])
            self.assertIn('purchased_by',
                          actual.data[i]['cow'])
            self.assertIn('purchase_date',
                          actual.data[i]['cow'])
            self.assertIn('breed',
                          actual.data[i]['cow'])
            self.assertIn('color',
                          actual.data[i]['cow'])
            self.assertIn('link',
                          actual.data[i]['cow'])
            self.assertIn('action',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestEventWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow',
                'action', 'event']

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
                           'client': cow.client,
                           'event_time': TestTime.get_datetime(),
                           'action': action.name}

    def test_00_load_fixtures(self):
        actions = Action.objects.all()
        self.assertLessEqual(17,
                             len(actions))
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        events = Event.objects.all()
        self.assertLessEqual(10,
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
        self.assertIn('client',
                      actual.data)
        self.assertIn('event_time',
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
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('cow',
                          actual.data[i])
            self.assertIn('event_time',
                          actual.data[i])
            self.assertIn('action',
                          actual.data[i])

    def test_03_full_update(self):
        event = Event.objects.get(id=1)
        self._load_event_data()
        self.event_data.update({'cow': event.cow.rfid,
                                'client': event.cow.client})
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
        self.assertEqual(self.event_data['client'].name,
                         actual.data['client'])
        self.assertIn('event_time',
                      actual.data)
        self.assertEqual(self.event_data['action'],
                         actual.data['action'])

    def test_04_partial_update(self):
        event = Event.objects.get(id=1)
        self._load_event_data()
        self.event_data.update({'cow': event.cow.rfid,
                                'client': event.cow.client})
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
        self.assertEqual(self.event_data['client'].name,
                         actual.data['client'])
        self.assertIn('event_time',
                      actual.data)
        self.assertEqual(event.action.name,
                         actual.data['action'])

class TestHealthRecordReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow', 'illness',
                'injury', 'status', 'treatment', 'vaccine', 'healthrecord']

    def setUp(self):
        self._load_model_data()

    def tearDown(self):
        self.model_data = None

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        illnesses = Illness.objects.all()
        illness = illnesses[randint(0, len(illnesses) - 1)]
        injuries = Injury.objects.all()
        injury = injuries[randint(0, len(injuries) - 1)]
        statuses = Status.objects.all()
        status = statuses[randint(0, len(statuses) - 1)]
        treatments = Treatment.objects.all()
        treatment = treatments[randint(0, len(treatments) - 1)]
        vaccines = Vaccine.objects.all()
        vaccine = vaccines[randint(0, len(vaccines) - 1)]
        self.model_data = {'recorded_by': user,
                           'cow': cow,
                           'client': cow.client,
                           'inspection_time': TestTime.get_datetime(),
                           'temperature': TestData.get_temp(),
                           'respiratory_rate': TestData.get_resp(),
                           'heart_rate': TestData.get_hr(),
                           'blood_pressure': TestData.get_bp(),
                           'weight': TestData.get_weight(),
                           'body_condition_score': TestData.get_bcs(),
                           'status': status,
                           'illness': illness,
                           'injury': injury,
                           'treatment': treatment,
                           'vaccine': vaccine}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        illnesses = Illness.objects.all()
        self.assertLessEqual(15,
                             len(illnesses))
        injuries = Injury.objects.all()
        self.assertLessEqual(5,
                             len(injuries))
        statuses = Status.objects.all()
        self.assertLessEqual(5,
                             len(statuses))
        treatments = Treatment.objects.all()
        self.assertLessEqual(14,
                             len(treatments))
        vaccines = Vaccine.objects.all()
        self.assertLessEqual(6,
                             len(vaccines))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        healthrecords = HealthRecord.objects.all()
        self.assertLessEqual(10,
                             len(healthrecords))

    def test_01_retrieve(self):
        health_record = HealthRecord.objects.get(pk=1)
        actual = HealthRecordReadSerializer(health_record)
        self.assertGreaterEqual(10,
                                actual.data['id'])
        self.assertRegex(actual.data['client']['name'],
                         '\w')
        self.assertRegex(actual.data['recorded_by'],
                         '\w')
        if actual.data['inspection_time'].find('.') > 0:
            self.assertRegex(actual.data['inspection_time'],
                             '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$')
        else:
            self.assertRegex(actual.data['inspection_time'],
                             '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}$')
        self.assertGreaterEqual(10,
                                actual.data['cow']['id'])
        self.assertRegex(actual.data['cow']['rfid'],
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertRegex(actual.data['cow']['purchased_by'],
                         '\w')
        self.assertRegex(actual.data['cow']['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['cow']['age']['name'],
                         '\d year')
        self.assertRegex(actual.data['cow']['breed']['name'],
                         '\w')
        self.assertRegex(actual.data['cow']['color']['name'],
                         '\w_\w')
        self.assertRegex(actual.data['cow']['link'],
                         '/assets/api/cows/\d/')
        self.assertRegex(str(actual.data['temperature']),
                         '\d{3}\.\d')
        self.assertRegex(str(actual.data['respiratory_rate']),
                         '\d{2}\.\d')
        self.assertRegex(str(actual.data['heart_rate']),
                         '\d{2}\.\d')
        self.assertRegex(str(actual.data['blood_pressure']),
                         '\d{3}\.\d')
        self.assertRegex(str(actual.data['weight']),
                         '\d{3}')
        self.assertRegex(str(actual.data['body_condition_score']),
                         '\d\.\d')
        self.assertRegex(actual.data['status']['name'],
                         '\w+')
        for attr in ['illness', 'injury', 'vaccine']:
            if attr in actual.data and actual.data[attr]:
                self.assertRegex(actual.data[attr],
                                 '\w+')
        self.assertRegex(actual.data['link'],
                         '/assets/api/healthrecords/\d/')

    def test_02_list(self):
        expected = 10
        health_records = []
        for i in range(expected):
            self._load_model_data()
            health_record = HealthRecord.objects.create(**self.model_data)
            health_records.append(health_record)
        actual = HealthRecordReadSerializer(health_records,
                                            many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('inspection_time',
                          actual.data[i])
            self.assertIn('id',
                          actual.data[i]['cow'])
            self.assertIn('rfid',
                          actual.data[i]['cow'])
            self.assertIn('purchased_by',
                          actual.data[i]['cow'])
            self.assertIn('purchase_date',
                          actual.data[i]['cow'])
            self.assertIn('age',
                          actual.data[i]['cow'])
            self.assertIn('breed',
                          actual.data[i]['cow'])
            self.assertIn('color',
                          actual.data[i]['cow'])
            self.assertIn('link',
                          actual.data[i]['cow'])
            self.assertIn('temperature',
                          actual.data[i])
            self.assertIn('respiratory_rate',
                          actual.data[i])
            self.assertIn('heart_rate',
                          actual.data[i])
            self.assertIn('blood_pressure',
                          actual.data[i])
            self.assertIn('weight',
                          actual.data[i])
            self.assertIn('body_condition_score',
                          actual.data[i])
            self.assertIn('status',
                          actual.data[i])
            self.assertIn('illness',
                          actual.data[i])
            self.assertIn('injury',
                          actual.data[i])
            self.assertIn('vaccine',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestHealthRecordWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow', 'illness',
                'injury', 'status', 'treatment', 'vaccine', 'healthrecord']

    def setUp(self):
        self._load_hr_data()

    def tearDown(self):
        self.hr_data = None

    def _load_hr_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.hr_data = {'recorded_by': user,
                        'cow': cow.rfid,
                        'client': cow.client,
                        'inspection_time': TestTime.get_datetime(),
                        'temperature': TestData.get_temp(),
                        'respiratory_rate': TestData.get_resp(),
                        'heart_rate': TestData.get_hr(),
                        'blood_pressure': TestData.get_bp(),
                        'weight': TestData.get_weight(),
                        'body_condition_score': TestData.get_bcs(),
                        'status': 'Healthy'}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        illnesses = Illness.objects.all()
        self.assertLessEqual(15,
                             len(illnesses))
        injuries = Injury.objects.all()
        self.assertLessEqual(5,
                             len(injuries))
        statuses = Status.objects.all()
        self.assertLessEqual(5,
                             len(statuses))
        vaccines = Vaccine.objects.all()
        self.assertLessEqual(6,
                             len(vaccines))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        healthrecords = HealthRecord.objects.all()
        self.assertLessEqual(10,
                             len(healthrecords))

    def test_01_create_healthy(self):
        actual = HealthRecordWriteSerializer(data=self.hr_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('client',
                      actual.data)
        self.assertIn('recorded_by',
                      actual.data)
        self.assertIn('cow',
                      actual.data)
        self.assertIn('inspection_time',
                      actual.data)
        self.assertIn('temperature',
                      actual.data)
        self.assertIn('respiratory_rate',
                      actual.data)
        self.assertIn('heart_rate',
                      actual.data)
        self.assertIn('blood_pressure',
                      actual.data)
        self.assertIn('weight',
                      actual.data)
        self.assertIn('body_condition_score',
                      actual.data)
        self.assertIn('status',
                      actual.data)
        self.assertIn('illness',
                      actual.data)
        self.assertIn('injury',
                      actual.data)
        self.assertIn('vaccine',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_hr_data()
            data.append(self.hr_data)
        actual = HealthRecordWriteSerializer(data=data,
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
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('cow',
                          actual.data[i])
            self.assertIn('inspection_time',
                          actual.data[i])
            self.assertIn('temperature',
                          actual.data[i])
            self.assertIn('respiratory_rate',
                          actual.data[i])
            self.assertIn('heart_rate',
                          actual.data[i])
            self.assertIn('blood_pressure',
                          actual.data[i])
            self.assertIn('weight',
                          actual.data[i])
            self.assertIn('body_condition_score',
                          actual.data[i])
            self.assertIn('status',
                          actual.data[i])
            self.assertIn('illness',
                          actual.data[i])
            self.assertIn('injury',
                          actual.data[i])
            self.assertIn('vaccine',
                          actual.data[i])

    def test_03_full_update(self):
        health_record = HealthRecord.objects.get(id=1)
        self._load_hr_data()
        illnesses = Illness.objects.all()
        illness = illnesses[randint(0, len(illnesses) - 1)]
        self.hr_data.update({'cow': health_record.cow.rfid,
                             'client': health_record.cow.client,
                             'illness': illness.diagnosis,
                             'status': Status.objects.get(name='Viral Illness'),
                             'treatment': Treatment.objects.get(name=illness.treatment).name})
        actual = HealthRecordWriteSerializer(health_record,
                                             data=self.hr_data,
                                             partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.hr_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.hr_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.hr_data['cow'],
                         actual.data['cow'])
        self.assertRegex(actual.data['inspection_time'],
                         '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-\d{2}:\d{2}$')
        self.assertRegex(str(actual.data['temperature']),
                         '\d{3}\.\d')
        self.assertRegex(str(actual.data['respiratory_rate']),
                         '\d{2}\.\d')
        self.assertRegex(str(actual.data['heart_rate']),
                         '\d{2}\.\d')
        self.assertRegex(str(actual.data['blood_pressure']),
                         '\d{3}\.\d')
        self.assertRegex(str(actual.data['weight']),
                         '\d{3}')
        self.assertRegex(str(actual.data['body_condition_score']),
                         '\d\.\d')
        self.assertRegex(actual.data['status'],
                         '\w+')
        for attr in ['illness', 'vaccine']:
            if attr in actual.data and actual.data[attr]:
                self.assertRegex(actual.data[attr],
                                 '\w+')

    def test_04_partial_update(self):
        health_record = HealthRecord.objects.get(id=1)
        self._load_hr_data()
        injuries = Injury.objects.all()
        injury = injuries[randint(0, len(injuries) - 1)]
        treatments = Treatment.objects.all()
        treatment = treatments[randint(0, len(treatments) - 1)]
        self.hr_data.update({'cow': health_record.cow.rfid,
                             'client': health_record.cow.client,
                             'injury': injury.diagnosis,
                             'status': Status.objects.get(name='Injured'),
                             'treatment': Treatment.objects.get(name=injury.treatment).name})
        del self.hr_data['weight']
        del self.hr_data['temperature']
        actual = HealthRecordWriteSerializer(health_record,
                                             data=self.hr_data,
                                             partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.hr_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.hr_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.hr_data['cow'],
                         actual.data['cow'])
        self.assertRegex(actual.data['inspection_time'],
                         '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-\d{2}:\d{2}$')
        self.assertRegex(str(health_record.temperature),
                         '\d{3}\.\d')
        self.assertRegex(str(actual.data['respiratory_rate']),
                         '\d{2}\.\d')
        self.assertRegex(str(actual.data['heart_rate']),
                         '\d{2}\.\d')
        self.assertRegex(str(actual.data['blood_pressure']),
                         '\d{3}\.\d')
        self.assertRegex(str(health_record.weight),
                         '\d{3}')
        self.assertRegex(str(actual.data['body_condition_score']),
                         '\d\.\d')
        self.assertRegex(actual.data['status'],
                         '\w+')
        for attr in ['injury', 'treatment', 'vaccine']:
            if attr in actual.data and actual.data[attr]:
                self.assertRegex(actual.data[attr],
                                 '\w+')

class TestMilkReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow', 'milk']

    def setUp(self):
        self._load_model_data()

    def tearDown(self):
        self.model_data = None

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.model_data = {'recorded_by': user,
                           'cow': cow,
                           'client': cow.client,
                           'milking_time': TestTime.get_datetime(),
                           'gallons': TestData.get_milk()}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        dairy = Milk.objects.all()
        self.assertLessEqual(10,
                             len(dairy))

    def test_01_retrieve(self):
        dairy = Milk.objects.get(pk=1)
        actual = MilkReadSerializer(dairy)
        self.assertGreaterEqual(10,
                                actual.data['id'])
        self.assertRegex(actual.data['client']['name'],
                         '\w')
        self.assertRegex(actual.data['recorded_by'],
                         '\w')
        self.assertRegex(actual.data['milking_time'],
                         '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}$')
        self.assertGreaterEqual(10,
                                actual.data['cow']['id'])
        self.assertRegex(actual.data['cow']['rfid'],
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertRegex(actual.data['cow']['purchased_by'],
                         '\w')
        self.assertRegex(actual.data['cow']['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['cow']['age']['name'],
                         '\d year')
        self.assertRegex(actual.data['cow']['breed']['name'],
                         '\w')
        self.assertRegex(actual.data['cow']['color']['name'],
                         '\w_\w')
        self.assertRegex(actual.data['cow']['link'],
                         '/assets/api/cows/\d/')
        self.assertGreaterEqual(10,
                                actual.data['gallons'])
        self.assertRegex(actual.data['link'],
                         '/assets/api/milk/\d/')

    def test_02_list(self):
        expected = 10
        dairy = []
        for i in range(expected):
            self._load_model_data()
            milk = Milk.objects.create(**self.model_data)
            dairy.append(milk)
        actual = MilkReadSerializer(dairy,
                                    many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('milking_time',
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
            self.assertIn('link',
                          actual.data[i]['cow'])
            self.assertIn('gallons',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestMilkWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow', 'milk']

    def setUp(self):
        self._load_milk_data()

    def tearDown(self):
        self.milk_data = None

    def _load_milk_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.milk_data = {'recorded_by': user,
                          'cow': cow.rfid,
                          'client': cow.client,
                          'milking_time': TestTime.get_datetime(),
                          'gallons': TestData.get_milk()}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        dairy = Milk.objects.all()
        self.assertLessEqual(10,
                             len(dairy))

    def test_01_create(self):
        actual = MilkWriteSerializer(data=self.milk_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('client',
                      actual.data)
        self.assertIn('recorded_by',
                      actual.data)
        self.assertIn('cow',
                      actual.data)
        self.assertIn('milking_time',
                      actual.data)
        self.assertIn('gallons',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_milk_data()
            data.append(self.milk_data)
        actual = MilkWriteSerializer(data=data,
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
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('cow',
                          actual.data[i])
            self.assertIn('milking_time',
                          actual.data[i])
            self.assertIn('gallons',
                          actual.data[i])

    def test_03_full_update(self):
        milk = Milk.objects.get(id=1)
        self._load_milk_data()
        self.milk_data.update({'cow': milk.cow.rfid,
                               'client': milk.cow.client})
        actual = MilkWriteSerializer(milk,
                                     data=self.milk_data,
                                     partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.milk_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.milk_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.milk_data['cow'],
                         actual.data['cow'])
        self.assertIn('milking_time',
                      actual.data)
        self.assertEqual(self.milk_data['gallons'],
                         actual.data['gallons'])

    def test_04_partial_update(self):
        milk = Milk.objects.get(id=1)
        self._load_milk_data()
        self.milk_data.update({'cow': milk.cow.rfid,
                               'client': milk.cow.client})
        del self.milk_data['gallons']
        actual = MilkWriteSerializer(milk,
                                     data=self.milk_data,
                                     partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.milk_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.milk_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.milk_data['cow'],
                         actual.data['cow'])
        self.assertIn('milking_time',
                      actual.data)
        self.assertEqual(milk.gallons,
                         actual.data['gallons'])

class TestSeedReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['user', 'cerealhay', 'grasshay', 'legumehay', 'pasture',
                'season', 'client', 'seed']

    def setUp(self):
        self._load_model_data()

    def tearDown(self):
        self.model_data = None

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        clients = Client.objects.all()
        client = clients[randint(0, len(clients) - 1)]
        cereals = CerealHay.objects.all()
        cereal = cereals[randint(0, len(cereals) - 1)]
        grasses = GrassHay.objects.all()
        grass = grasses[randint(0, len(grasses) - 1)]
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        fields = Pasture.objects.filter(fallow=False)
        pasture = fields[randint(0, len(fields) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.model_data = {'season': season,
                           'year': TestTime.get_year(),
                           'client': client,
                           'seeded_by': user,
                           'pasture': pasture,
                           'cereal_hay': cereal,
                           'grass_hay': grass,
                           'legume_hay': legume}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        cereals = CerealHay.objects.all()
        self.assertLessEqual(5,
                             len(cereals))
        grasses = GrassHay.objects.all()
        self.assertLessEqual(9,
                             len(grasses))
        legumes = LegumeHay.objects.all()
        self.assertLessEqual(6,
                             len(legumes))
        pastures = Pasture.objects.all()
        self.assertLessEqual(13,
                             len(pastures))
        seasons = Season.objects.all()
        self.assertLessEqual(4,
                             len(seasons))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        seeds = Seed.objects.all()
        self.assertLessEqual(10,
                             len(seeds))

    def test_01_retrieve(self):
        seed = Seed.objects.get(id=1)
        actual = SeedReadSerializer(seed)
        self.assertEqual(actual.data['seeded_by'],
                         TestData.get_random_user())
        self.assertRegex(actual.data['client']['name'],
                         '^\w')
        self.assertLessEqual(2014,
                             actual.data['year'])
        self.assertRegex(actual.data['season']['name'],
                         '^\w+$')
        self.assertRegex(actual.data['pasture']['name'],
                         '^\w+$')
        self.assertFalse(actual.data['pasture']['fallow'])
        self.assertLessEqual(1,
                             actual.data['pasture']['distance'])
        self.assertRegex(actual.data['cereal_hay']['name'],
                         '^\w+$')
        self.assertRegex(actual.data['grass_hay']['name'],
                         '^\w+$')
        self.assertRegex(actual.data['legume_hay']['name'],
                         '^\w+$')

    def test_02_list(self):
        expected = 10
        seeds = []
        for i in range(expected):
            self._load_model_data()
            seed = Seed.objects.create(**self.model_data)
            seeds.append(seed)
        actual = SeedReadSerializer(seeds,
                                    many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('year',
                          actual.data[i])
            self.assertIn('season',
                          actual.data[i])
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('seeded_by',
                          actual.data[i])
            self.assertIn('pasture',
                          actual.data[i])
            self.assertIn('cereal_hay',
                          actual.data[i])
            self.assertIn('grass_hay',
                          actual.data[i])
            self.assertIn('legume_hay',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestSeedWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['user', 'cerealhay', 'grasshay', 'legumehay', 'pasture',
                'season', 'client', 'seed']

    def setUp(self):
        self._load_seed_data()

    def tearDown(self):
        self.seed_data = None

    def _load_seed_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        clients = Client.objects.all()
        client = clients[randint(0, len(clients) - 1)]
        cereals = CerealHay.objects.all()
        cereal = cereals[randint(0, len(cereals) - 1)]
        grasses = GrassHay.objects.all()
        grass = grasses[randint(0, len(grasses) - 1)]
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        fields = Pasture.objects.filter(fallow=False)
        pasture = fields[randint(0, len(fields) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.seed_data = {'season': season,
                          'year': TestTime.get_year(),
                          'client': client,
                          'seeded_by': user,
                          'pasture': pasture.name,
                          'cereal_hay': cereal.name,
                          'grass_hay': grass.name,
                          'legume_hay': legume.name}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        cereals = CerealHay.objects.all()
        self.assertLessEqual(5,
                             len(cereals))
        grasses = GrassHay.objects.all()
        self.assertLessEqual(9,
                             len(grasses))
        legumes = LegumeHay.objects.all()
        self.assertLessEqual(6,
                             len(legumes))
        pastures = Pasture.objects.all()
        self.assertLessEqual(13,
                             len(pastures))
        seasons = Season.objects.all()
        self.assertLessEqual(4,
                             len(seasons))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))
        seeds = Seed.objects.all()
        self.assertLessEqual(10,
                             len(seeds))

    def test_01_create(self):
        actual = SeedWriteSerializer(data=self.seed_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertRegex(actual.data['pasture'],
                         '\w+')
        self.assertIn('year',
                      actual.data)
        self.assertIn('season',
                      actual.data)
        self.assertIn('client',
                      actual.data)
        self.assertIn('seeded_by',
                      actual.data)
        self.assertIn('cereal_hay',
                      actual.data)
        self.assertIn('grass_hay',
                      actual.data)
        self.assertIn('legume_hay',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_seed_data()
            data.append(self.seed_data)
        actual = SeedWriteSerializer(data=data,
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
            self.assertRegex(actual.data[i]['client'],
                             '\w+')
            self.assertRegex(actual.data[i]['pasture'],
                             '\w+')
            self.assertIn('year',
                          actual.data[i])
            self.assertIn('season',
                          actual.data[i])
            self.assertIn('seeded_by',
                          actual.data[i])
            self.assertIn('cereal_hay',
                          actual.data[i])
            self.assertIn('grass_hay',
                          actual.data[i])
            self.assertIn('legume_hay',
                          actual.data[i])

    def test_03_full_update(self):
        seed = Seed.objects.get(id=1)
        self._load_seed_data()
        actual = SeedWriteSerializer(seed,
                                     data=self.seed_data,
                                     partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.seed_data['year'],
                         actual.data['year'])
        self.assertEqual(self.seed_data['season'].name,
                         actual.data['season'])
        self.assertEqual(self.seed_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.seed_data['seeded_by'].username,
                         actual.data['seeded_by'])
        self.assertEqual(self.seed_data['pasture'],
                         actual.data['pasture'])
        self.assertEqual(self.seed_data['cereal_hay'],
                         actual.data['cereal_hay'])
        self.assertEqual(self.seed_data['grass_hay'],
                         actual.data['grass_hay'])
        self.assertEqual(self.seed_data['legume_hay'],
                         actual.data['legume_hay'])

    def test_04_partial_update(self):
        seed = Seed.objects.get(id=1)
        self._load_seed_data()
        del self.seed_data['pasture']
        actual = SeedWriteSerializer(seed,
                                     data=self.seed_data,
                                     partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.seed_data['year'],
                         actual.data['year'])
        self.assertEqual(self.seed_data['season'].name,
                         actual.data['season'])
        self.assertEqual(self.seed_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.seed_data['seeded_by'].username,
                         actual.data['seeded_by'])
        self.assertEqual(seed.pasture.name,
                         actual.data['pasture'])
        self.assertEqual(self.seed_data['cereal_hay'],
                         actual.data['cereal_hay'])
        self.assertEqual(self.seed_data['grass_hay'],
                         actual.data['grass_hay'])
        self.assertEqual(self.seed_data['legume_hay'],
                         actual.data['legume_hay'])

class TestExerciseReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow', 'pasture',
                'exercise']

    def setUp(self):
        self._load_model_data()

    def tearDown(self):
        self.model_data = None

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        fields = Pasture.objects.all()
        pasture = fields[randint(0, len(fields) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        distance = TestData.get_distance()
        self.model_data = {'recorded_by': user,
                           'cow': cow,
                           'client': cow.client,
                           'exercise_time': TestTime.get_datetime(),
                           'pasture': pasture}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        exercises = Exercise.objects.all()
        self.assertLessEqual(10,
                             len(exercises))
        fields = Pasture.objects.all()
        self.assertLessEqual(13,
                             len(fields))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))

    def test_01_retrieve(self):
        exercise = Exercise.objects.get(pk=1)
        actual = ExerciseReadSerializer(exercise)
        self.assertGreaterEqual(10,
                                actual.data['id'])
        self.assertRegex(actual.data['client']['name'],
                         '\w')
        self.assertRegex(actual.data['recorded_by'],
                         '\w')
        self.assertRegex(actual.data['exercise_time'],
                         '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:\d{2}$')
        self.assertGreaterEqual(10,
                                actual.data['cow']['id'])
        self.assertRegex(actual.data['cow']['rfid'],
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertRegex(actual.data['cow']['purchased_by'],
                         '\w')
        self.assertRegex(actual.data['cow']['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['cow']['age']['name'],
                         '\d year')
        self.assertRegex(actual.data['cow']['breed']['name'],
                         '\w')
        self.assertRegex(actual.data['cow']['color']['name'],
                         '\w_\w')
        self.assertRegex(actual.data['cow']['link'],
                         '/assets/api/cows/\d/')
        self.assertLessEqual(1,
                             actual.data['pasture']['id'])
        self.assertIsInstance(actual.data['pasture']['fallow'],
                              bool)
        self.assertLessEqual(1,
                             actual.data['pasture']['distance'])
        self.assertRegex(actual.data['pasture']['name'],
                         '\w')
        self.assertRegex(actual.data['link'],
                         '/assets/api/exercises/\d+/')

    def test_02_list(self):
        expected = 10
        exercises = []
        for i in range(expected):
            self._load_model_data()
            exercise = Exercise.objects.create(**self.model_data)
            exercises.append(exercise)
        actual = ExerciseReadSerializer(exercises,
                                        many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('exercise_time',
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
            self.assertIn('link',
                          actual.data[i]['cow'])
            self.assertIn('id',
                          actual.data[i]['pasture'])
            self.assertIn('fallow',
                          actual.data[i]['pasture'])
            self.assertIn('name',
                          actual.data[i]['pasture'])
            self.assertIn('distance',
                          actual.data[i]['pasture'])
            self.assertIn('link',
                          actual.data[i])

class TestExerciseWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'user', 'color', 'client', 'cow', 'pasture',
                'exercise']

    def setUp(self):
        self._load_exercise_data()

    def tearDown(self):
        self.exercise_data = None

    def _load_exercise_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        fields = Pasture.objects.all()
        pasture = fields[randint(0, len(fields) - 1)]
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        self.exercise_data = {'recorded_by': user,
                              'cow': cow.rfid,
                              'client': cow.client,
                              'exercise_time': TestTime.get_datetime(),
                              'pasture': pasture}

    def test_00_load_fixtures(self):
        clients = Client.objects.all()
        self.assertLessEqual(5,
                             len(clients))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        exercises = Exercise.objects.all()
        self.assertLessEqual(10,
                             len(exercises))
        fields = Pasture.objects.all()
        self.assertLessEqual(13,
                             len(fields))
        users = User.objects.all()
        self.assertLessEqual(4,
                             len(users))

    def test_01_create(self):
        actual = ExerciseWriteSerializer(data=self.exercise_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('recorded_by',
                      actual.data)
        self.assertIn('client',
                      actual.data)
        self.assertIn('cow',
                      actual.data)
        self.assertIn('pasture',
                      actual.data)
        self.assertIn('exercise_time',
                      actual.data)

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_exercise_data()
            data.append(self.exercise_data)
        actual = ExerciseWriteSerializer(data=data,
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
            self.assertIn('client',
                          actual.data[i])
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('cow',
                          actual.data[i])
            self.assertIn('pasture',
                          actual.data[i])
            self.assertIn('exercise_time',
                          actual.data[i])

    def test_03_full_update(self):
        exercise = Exercise.objects.get(id=1)
        self._load_exercise_data()
        self.exercise_data.update({'cow': exercise.cow.rfid,
                                   'client': exercise.cow.client})
        actual = ExerciseWriteSerializer(exercise,
                                         data=self.exercise_data,
                                         partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.exercise_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.exercise_data['cow'],
                         actual.data['cow'])
        self.assertEqual(self.exercise_data['client'].name,
                         actual.data['client'])
        self.assertEqual(self.exercise_data['pasture'].name,
                         actual.data['pasture'])
        self.assertIn('exercise_time',
                      actual.data)

    def test_04_partial_update(self):
        exercise = Exercise.objects.get(id=1)
        self._load_exercise_data()
        self.exercise_data.update({'cow': exercise.cow.rfid,
                                   'client': exercise.cow.client})
        del self.exercise_data['pasture']
        actual = ExerciseWriteSerializer(exercise,
                                         data=self.exercise_data,
                                         partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.exercise_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.exercise_data['cow'],
                         actual.data['cow'])
        self.assertEqual(self.exercise_data['client'].name,
                         actual.data['client'])
        self.assertEqual(exercise.pasture.name,
                         actual.data['pasture'])
        self.assertIn('exercise_time',
                      actual.data)


