from random import randint

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from assets.models import Action, Age, Breed, CerealHay, Color, Cow
from assets.models import Event, Exercise, GrassHay, HealthRecord, Illness
from assets.models import Injury, LegumeHay, Milk, Pasture, Season
from assets.models import Seed, Status, Treatment, Vaccine
from assets.serializers import ActionSerializer, AgeSerializer
from assets.serializers import BreedSerializer, ColorSerializer
from assets.serializers import CerealHaySerializer, GrassHaySerializer
from assets.serializers import IllnessSerializer, InjurySerializer
from assets.serializers import LegumeHaySerializer, PastureSerializer
from assets.serializers import SeasonSerializer, StatusSerializer
from assets.serializers import TreatmentSerializer, VaccineSerializer

from assets.serializers import CowReadSerializer, CowWriteSerializer
from assets.serializers import EventReadSerializer, EventWriteSerializer, ExerciseReadSerializer
from assets.serializers import ExerciseWriteSerializer
from assets.serializers import HealthRecordReadSerializer
from assets.serializers import HealthRecordWriteSerializer, MilkReadSerializer
from assets.serializers import MilkWriteSerializer, PastureSerializer
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
        self.assertEqual(17,
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
        self.age_data = {'name': '{} years'.format(randint(10, 1000))}

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))

    def test_01_create(self):
        actual = AgeSerializer(data=self.age_data)
        self.assertTrue(actual.is_valid())
        print(actual.errors)
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
        name = '{}_{}'.format(TestData.get_breed(), randint(10, 1000))
        self.breed_data = {'name': name,
                           'url': '/static/images/breeds/{}.jpg'.format(name.lower())}

    def test_00_load_fixtures(self):
        breeds = Breed.objects.all()
        self.assertEqual(7,
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

class TestColorSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['color']

    def setUp(self):
        self._load_color_data()

    def tearDown(self):
        self.color_data = None

    def _load_color_data(self):
        name = '{}_{}'.format(TestData.get_color(), randint(10, 1000))
        self.color_data = {'name': name}

    def test_00_load_fixtures(self):
        colors = Color.objects.all()
        self.assertEqual(9,
                         len(colors))

    def test_01_create(self):
        actual = ColorSerializer(data=self.color_data)
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
            self._load_color_data()
            self.color_data.update({'name': '{} {}'.format(self.color_data['name'], i)})
            data.append(self.color_data)
        actual = ColorSerializer(data=data,
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
        color = Color.objects.get(id=1)
        actual = ColorSerializer(color)
        self.assertRegex(actual.data['name'],
                         '\w+')

    def test_04_list(self):
        expected = 10
        colors = []
        for i in range(expected):
            self._load_color_data()
            self.color_data.update({'name': '{} {}'.format(self.color_data['name'], i)})
            color = Color.objects.create(**self.color_data)
            colors.append(color)
        actual = ColorSerializer(colors,
                                  many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('name',
                          actual.data[i])

    def test_05_full_update(self):
        color = Color.objects.get(id=1)
        self._load_color_data()
        actual = ColorSerializer(color,
                                  data=self.color_data,
                                  partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.color_data['name'],
                         actual.data['name'])

class TestCerealHaySerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['cerealhay']

    def setUp(self):
        self._load_cereal_data()

    def tearDown(self):
        self.cereal_data = None

    def _load_cereal_data(self):
        name = '{}_{}'.format(TestData.get_cereal(), randint(10, 1000))
        self.cereal_data = {'name': name}

    def test_00_load_fixtures(self):
        cereals = CerealHay.objects.all()
        self.assertEqual(5,
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
        name = '{}_{}'.format(TestData.get_grass(), randint(10, 1000))
        self.grass_data = {'name': name}

    def test_00_load_fixtures(self):
        grasses = GrassHay.objects.all()
        self.assertEqual(9,
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
        diagnosis = '{}_{}'.format(TestData.get_illness(), randint(10, 1000))
        treatment = '{}_{}'.format(TestData.get_treatment(), randint(10, 1000))
        self.illness_data = {'diagnosis': diagnosis,
                             'treatment': treatment}

    def test_00_load_fixtures(self):
        illnesses = Illness.objects.all()
        self.assertEqual(15,
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
        self.assertEqual(5,
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
        name = '{}_{}'.format(TestData.get_legume(), randint(10, 1000))
        self.legume_data = {'name': name}

    def test_00_load_fixtures(self):
        legumes = LegumeHay.objects.all()
        self.assertEqual(6,
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

class TestSeasonSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['season']

    def setUp(self):
        self._load_season_data()

    def tearDown(self):
        self.season_data = None

    def _load_season_data(self):
        name = '{}_{}'.format(TestData.get_season(), randint(10, 1000))
        self.season_data = {'name': name}

    def test_00_load_fixtures(self):
        seasons = Season.objects.all()
        self.assertEqual(4,
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
        name = '{}_{}'.format(TestData.get_status(), randint(10, 1000))
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
        name = '{}_{}'.format('apply_salve', randint(10, 1000))
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
        name = '{}_{}'.format('take vaccine', randint(10, 1000))
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
    fixtures = ['age', 'breed', 'color', 'user', 'cow']

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
        self.cow_data = {'purchased_by': user,
                         'purchased_date': TestTime.get_date(),
                         'age': age.name,
                         'breed': breed.name,
                         'color': color.name}

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        ages = Age.objects.all()
        age = ages[randint(0, len(ages) - 1)]
        breeds = Breed.objects.all()
        breed = breeds[randint(0, len(breeds) - 1)]
        colors = Color.objects.all()
        color = colors[randint(0, len(colors) - 1)]
        self.model_data = {'purchased_by': user,
                           'purchased_date': TestTime.get_date(),
                           'age': age,
                           'breed': breed,
                           'color': color}

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))
        breeds = Breed.objects.all()
        self.assertEqual(5,
                         len(breeds))
        colors = Color.objects.all()
        self.assertEqual(5,
                         len(colors))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))

    def test_01_create(self):
        actual = CowReadSerializer(data=self.cow_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('name',
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
        self.assertIn('link',
                      actual.data)

    def test_06_partial_update(self):
        cow = Cow.objects.get(id=1)
        self._load_cow_data()
        del self.cow_data['purchase_date']
        del self.cow_data['breed']
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
        self.assertIn('link',
                      actual.data)

class TestPastureSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['pasture']

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
        legumes = LegumeHay.objects.all()
        legume = legumes[randint(0, len(legumes) - 1)]
        regions = Region.objects.all()
        region = regions[randint(0, len(regions) - 1)]
        seasons = Season.objects.all()
        season = seasons[randint(0, len(seasons) - 1)]
        self.pasture_data = {'fallow': fallow,
                             'distance': distance,
                             'season': season,
                             'year': TestTime.get_year(),
                             'seeded_by': user,
                             'region': region.name,
                             'cereal_hay': cereal.name,
                             'grass_hay': grass.name,
                             'legume_hay': legume.name}

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_user())
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
        self.model_data = {'fallow': fallow,
                           'distance': distance,
                           'season': season,
                           'year': TestTime.get_year(),
                           'seeded_by': user,
                           'region': region,
                           'cereal_hay': cereal,
                           'grass_hay': grass,
                           'legume_hay': legume}

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
        self.assertIn('year',
                      actual.data)
        self.assertIn('season',
                      actual.data)
        self.assertIn('seeded_by',
                      actual.data)
        self.assertIn('region',
                      actual.data)
        self.assertIn('cereal_hay',
                      actual.data)
        self.assertIn('grass_hay',
                      actual.data)
        self.assertIn('legume_hay',
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
            self.assertIn('year',
                          actual.data[i])
            self.assertIn('season',
                          actual.data[i])
            self.assertIn('distance',
                          actual.data[i])
            self.assertIn('seeded_by',
                          actual.data[i])
            self.assertIn('region',
                          actual.data[i])
            self.assertIn('cereal_hay',
                          actual.data[i])
            self.assertIn('grass_hay',
                          actual.data[i])
            self.assertIn('legume_hay',
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
        self.assertLessEqual(2014,
                             actual.data['year'])
        self.assertRegex(actual.data['season'],
                         '^\w+$')
        self.assertRegex(actual.data['region'],
                         '^\w+$')
        self.assertRegex(actual.data['cereal_hay'],
                         '^\w+$')
        self.assertRegex(actual.data['grass_hay'],
                         '^\w+$')
        self.assertRegex(actual.data['legume_hay'],
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
            self.assertIn('year',
                          actual.data[i])
            self.assertIn('season',
                          actual.data[i])
            self.assertIn('distance',
                          actual.data[i])
            self.assertIn('seeded_by',
                          actual.data[i])
            self.assertIn('region',
                          actual.data[i])
            self.assertIn('cereal_hay',
                          actual.data[i])
            self.assertIn('grass_hay',
                          actual.data[i])
            self.assertIn('legume_hay',
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
        self.assertEqual(self.pasture_data['year'],
                         actual.data['year'])
        self.assertEqual(self.pasture_data['season'].name,
                         actual.data['season'])
        self.assertEqual(self.pasture_data['distance'],
                         actual.data['distance'])
        self.assertEqual(self.pasture_data['seeded_by'].username,
                         actual.data['seeded_by'])
        self.assertEqual(self.pasture_data['region'],
                         actual.data['region'])
        self.assertEqual(self.pasture_data['cereal_hay'],
                         actual.data['cereal_hay'])
        self.assertEqual(self.pasture_data['grass_hay'],
                         actual.data['grass_hay'])
        self.assertEqual(self.pasture_data['legume_hay'],
                         actual.data['legume_hay'])

    def test_06_partial_update(self):
        pasture = Pasture.objects.get(id=1)
        self._load_pasture_data()
        del self.pasture_data['distance']
        del self.pasture_data['region']
        actual = PastureSerializer(pasture,
                                   data=self.pasture_data,
                                   partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.pasture_data['fallow'],
                         actual.data['fallow'])
        self.assertEqual(self.pasture_data['year'],
                         actual.data['year'])
        self.assertEqual(self.pasture_data['season'].name,
                         actual.data['season'])
        self.assertEqual(pasture.distance,
                         actual.data['distance'])
        self.assertEqual(self.pasture_data['seeded_by'].username,
                         actual.data['seeded_by'])
        self.assertEqual(pasture.region.name,
                         actual.data['region'])
        self.assertEqual(self.pasture_data['cereal_hay'],
                         actual.data['cereal_hay'])
        self.assertEqual(self.pasture_data['grass_hay'],
                         actual.data['grass_hay'])
        self.assertEqual(self.pasture_data['legume_hay'],
                         actual.data['legume_hay'])

class TestEventReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'user', 'cow', 'action', 'event']

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
        self.assertLessEqual(10,
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
                         '\d year')
        self.assertRegex(actual.data['cow']['breed'],
                         '\w')
        self.assertRegex(actual.data['cow']['color'],
                         '\w_\w')
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
            self.assertIn('link',
                          actual.data[i]['cow'])
            self.assertIn('action',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestEventWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
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

class TestMilkReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'user', 'cow', 'milk']

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
                           'gallons': TestData.get_milk()}

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        dairy = Milk.objects.all()
        self.assertLessEqual(10,
                             len(dairy))

    def test_01_retrieve(self):
        dairy = Milk.objects.get(pk=1)
        actual = MilkReadSerializer(dairy)
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
                         '\d year')
        self.assertRegex(actual.data['cow']['breed'],
                         '\w')
        self.assertRegex(actual.data['cow']['color'],
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
            self.assertIn('link',
                          actual.data[i]['cow'])
            self.assertIn('gallons',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestMilkWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'user', 'cow', 'milk']

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
                          'gallons': TestData.get_milk()}

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        users = User.objects.all()
        self.assertEqual(3,
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
        self.assertIn('recorded_by',
                      actual.data)
        self.assertIn('cow',
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
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('cow',
                          actual.data[i])
            self.assertIn('gallons',
                          actual.data[i])

    def test_03_full_update(self):
        milk = Milk.objects.get(id=1)
        self._load_milk_data()
        self.milk_data.update({'cow': milk.cow.rfid})
        actual = MilkWriteSerializer(milk,
                                     data=self.milk_data,
                                     partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.milk_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.milk_data['cow'],
                         actual.data['cow'])
        self.assertEqual(self.milk_data['gallons'],
                         actual.data['gallons'])

    def test_04_partial_update(self):
        milk = Milk.objects.get(id=1)
        self._load_milk_data()
        self.milk_data.update({'cow': milk.cow.rfid})
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
        self.assertEqual(self.milk_data['cow'],
                         actual.data['cow'])
        self.assertEqual(milk.gallons,
                         actual.data['gallons'])

class TestExerciseReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'cerealhay', 'grasshay', 'legumehay', 'region',
                'season', 'pasture', 'exercise']

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
                           'pasture': pasture,
                           'distance': distance}

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        exercises = Exercise.objects.all()
        self.assertLessEqual(10,
                             len(exercises))
        fields = Pasture.objects.all()
        self.assertEqual(13,
                         len(fields))

    def test_01_retrieve(self):
        exercise = Exercise.objects.get(pk=1)
        actual = ExerciseReadSerializer(exercise)
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
                         '\d year')
        self.assertRegex(actual.data['cow']['breed'],
                         '\w')
        self.assertRegex(actual.data['cow']['color'],
                         '\w_\w')
        self.assertRegex(actual.data['cow']['link'],
                         '/assets/api/cows/\d/')
        self.assertLessEqual(1,
                             actual.data['pasture']['id'])
        self.assertIsInstance(actual.data['pasture']['fallow'],
                              bool)
        self.assertGreaterEqual(5,
                                actual.data['pasture']['distance'])
        self.assertEqual(actual.data['pasture']['seeded_by'],
                         TestData.get_random_user())
        self.assertRegex(actual.data['pasture']['region'],
                         '^\w+')
        self.assertRegex(actual.data['pasture']['cereal_hay'],
                         '^\w+')
        self.assertRegex(actual.data['pasture']['grass_hay'],
                         '^\w+')
        self.assertRegex(actual.data['pasture']['legume_hay'],
                         '^\w+')
        self.assertRegex(actual.data['pasture']['link'],
                         '/assets/api/pastures/\d+/')
        self.assertGreaterEqual(10,
                                actual.data['distance'])
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
            self.assertIn('link',
                          actual.data[i]['cow'])
            self.assertIn('id',
                          actual.data[i]['pasture'])
            self.assertIn('fallow',
                          actual.data[i]['pasture'])
            self.assertIn('seeded_by',
                          actual.data[i]['pasture'])
            self.assertIn('region',
                          actual.data[i]['pasture'])
            self.assertIn('cereal_hay',
                          actual.data[i]['pasture'])
            self.assertIn('grass_hay',
                          actual.data[i]['pasture'])
            self.assertIn('legume_hay',
                          actual.data[i]['pasture'])
            self.assertIn('link',
                          actual.data[i]['pasture'])
            self.assertIn('distance',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestExerciseWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'cerealhay', 'grasshay', 'legumehay', 'region',
                'season', 'pasture', 'exercise']

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
        distance = TestData.get_distance()
        self.exercise_data = {'recorded_by': user,
                              'cow': cow.rfid,
                              'pasture': pasture.region.id,
                              'distance': distance}

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        exercises = Exercise.objects.all()
        self.assertLessEqual(10,
                             len(exercises))
        fields = Pasture.objects.all()
        self.assertEqual(13,
                         len(fields))

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
        self.assertIn('cow',
                      actual.data)
        self.assertIn('pasture',
                      actual.data)
        self.assertIn('distance',
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
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('cow',
                          actual.data[i])
            self.assertIn('pasture',
                          actual.data[i])
            self.assertIn('distance',
                          actual.data[i])

    def test_03_full_update(self):
        exercise = Exercise.objects.get(id=1)
        self._load_exercise_data()
        self.exercise_data.update({'cow': exercise.cow.rfid})
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
        self.assertEqual(self.exercise_data['pasture'],
                         actual.data['pasture'])
        self.assertEqual(self.exercise_data['distance'],
                         actual.data['distance'])

    def test_04_partial_update(self):
        exercise = Exercise.objects.get(id=1)
        self._load_exercise_data()
        self.exercise_data.update({'cow': exercise.cow.rfid})
        del self.exercise_data['pasture']
        del self.exercise_data['distance']
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
        self.assertEqual(exercise.pasture.region.id,
                         actual.data['pasture'])
        self.assertEqual(exercise.distance,
                         actual.data['distance'])

class TestHealthRecordReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'illness', 'injury', 'status', 'vaccine', 'healthrecord']

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
        vaccines = Vaccine.objects.all()
        vaccine = vaccines[randint(0, len(vaccines) - 1)]
        self.model_data = {'recorded_by': user,
                           'cow': cow,
                           'temperature': TestData.get_temp(),
                           'respiratory_rate': TestData.get_resp(),
                           'heart_rate': TestData.get_hr(),
                           'blood_pressure': TestData.get_bp(),
                           'weight': TestData.get_weight(),
                           'body_condition_score': TestData.get_bcs(),
                           'status': status,
                           'illness': illness,
                           'injury': injury,
                           'vaccine': vaccine}

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        illnesses = Illness.objects.all()
        self.assertEqual(15,
                         len(illnesses))
        injuries = Injury.objects.all()
        self.assertEqual(5,
                         len(injuries))
        statuses = Status.objects.all()
        self.assertEqual(5,
                         len(statuses))
        vaccines = Vaccine.objects.all()
        self.assertEqual(6,
                         len(vaccines))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        healthrecords = HealthRecord.objects.all()
        self.assertLessEqual(10,
                             len(healthrecords))

    def test_01_retrieve(self):
        health_record = HealthRecord.objects.get(pk=1)
        actual = HealthRecordReadSerializer(health_record)
        self.assertGreaterEqual(10,
                                actual.data['id'])
        self.assertRegex(actual.data['recorded_by'],
                         '\w')
        if actual.data['timestamp'].find('.') > 0:
            self.assertRegex(actual.data['timestamp'],
                             '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$')
        else:
            self.assertRegex(actual.data['timestamp'],
                             '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
        self.assertGreaterEqual(10,
                                actual.data['cow']['id'])
        self.assertRegex(actual.data['cow']['rfid'],
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertRegex(actual.data['cow']['purchased_by'],
                         '\w')
        self.assertRegex(actual.data['cow']['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['cow']['age'],
                         '\d year')
        self.assertRegex(actual.data['cow']['breed'],
                         '\w')
        self.assertRegex(actual.data['cow']['color'],
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
        self.assertRegex(actual.data['status'],
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
    fixtures = ['age', 'breed', 'color', 'user', 'cow',
                'illness', 'injury', 'status', 'vaccine', 'healthrecord']

    def setUp(self):
        self._load_hr_data()

    def tearDown(self):
        self.hr_data = None

    def _load_hr_data(self):
        user = User.objects.get(username=TestData.get_random_user())
        herd = Cow.objects.all()
        cow = herd[randint(0, len(herd) - 1)]
        #illnesses = Illness.objects.all()
        #illness = illnesses[randint(0, len(illnesses) - 1)]
        #injuries = Injury.objects.all()
        #injury = injuries[randint(0, len(injuries) - 1)]
        #statuses = Status.objects.all()
        #status = statuses[randint(0, len(statuses) - 1)]
        #vaccines = Vaccine.objects.all()
        #vaccine = vaccines[randint(0, len(vaccines) - 1)]
        self.hr_data = {'recorded_by': user,
                        'cow': cow.rfid,
                        'temperature': TestData.get_temp(),
                        'respiratory_rate': TestData.get_resp(),
                        'heart_rate': TestData.get_hr(),
                        'blood_pressure': TestData.get_bp(),
                        'weight': TestData.get_weight(),
                        'body_condition_score': TestData.get_bcs(),
                        'status': 'Healthy'}

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertEqual(130,
                         len(herd))
        illnesses = Illness.objects.all()
        self.assertEqual(15,
                         len(illnesses))
        injuries = Injury.objects.all()
        self.assertEqual(5,
                         len(injuries))
        statuses = Status.objects.all()
        self.assertEqual(5,
                         len(statuses))
        vaccines = Vaccine.objects.all()
        self.assertEqual(6,
                         len(vaccines))
        users = User.objects.all()
        self.assertEqual(3,
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
        self.assertIn('recorded_by',
                      actual.data)
        self.assertIn('cow',
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
        self.assertIn('link',
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
            self.assertIn('recorded_by',
                          actual.data[i])
            self.assertIn('cow',
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
            self.assertIn('link',
                          actual.data[i])

    def test_03_full_update(self):
        health_record = HealthRecord.objects.get(id=1)
        self._load_hr_data()
        self.hr_data.update({'cow': health_record.cow.rfid})
        actual = HealthRecordWriteSerializer(health_record,
                                             data=self.hr_data,
                                             partial=False)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.hr_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.hr_data['cow'],
                         actual.data['cow'])
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
        for attr in ['illness', 'injury', 'vaccine']:
            if attr in actual.data and actual.data[attr]:
                self.assertRegex(actual.data[attr],
                                 '\w+')
        self.assertRegex(actual.data['link'],
                         '/assets/api/healthrecords/\d/')

    def test_04_partial_update(self):
        health_record = HealthRecord.objects.get(id=1)
        self._load_hr_data()
        self.hr_data.update({'cow': health_record.cow.rfid})
        del self.hr_data['weight']
        del self.hr_data['temperature']
        actual = HealthRecordWriteSerializer(health_record,
                                             data=self.hr_data,
                                             partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertEqual(self.hr_data['recorded_by'].username,
                         actual.data['recorded_by'])
        self.assertEqual(self.hr_data['cow'],
                         actual.data['cow'])
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
        for attr in ['illness', 'injury', 'vaccine']:
            if attr in actual.data and actual.data[attr]:
                self.assertRegex(actual.data[attr],
                                 '\w+')
        self.assertRegex(actual.data['link'],
                         '/assets/api/healthrecords/\d/')

