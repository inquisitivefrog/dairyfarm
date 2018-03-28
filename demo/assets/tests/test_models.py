from random import randint

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from assets.models import Age, Action, Breed, Color, Cow
from assets.models import CerealHay, GrassHay, Illness, Injury, LegumeHay
from assets.models import Season, Seed, Status, Treatment
from assets.models import Vaccine, Pasture, HealthRecord, Milk, Event, Exercise
from assets.tests.utils import TestData, TestTime

class TestActionModel(APITestCase):
    fixtures = ['action']

    def setUp(self):
        self.action_data = {'name': TestData.get_action()}

    def tearDown(self):
        self.action_data = None

    def test_00_load_fixtures(self):
        actions = Action.objects.all()
        self.assertEqual(17,
                         len(actions))

    def test_01_object(self):
        a = Action()
        self.assertEqual("<class 'assets.models.Action'>",
                         repr(a))
        self.assertEqual("<class 'assets.models.Action'>",
                         str(a))
        a = Action.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Action'>:{}".format(a.id),
                         repr(a))
        self.assertEqual(a.name,
                         str(a))
 
    def test_02_get(self):
        a = Action.objects.get(id=1)
        self.assertEqual('Call Vet',
                         a.name)        

    def test_03_filter(self):
        expected = Action.objects.filter(name='Walk to pasture')
        actual = Action.objects.filter(name__endswith='pasture')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        a = Action.objects.create(**self.action_data)
        self.assertEqual(self.action_data['name'],
                         a.name)

    def test_05_full_update(self):
        expected = Action.objects.get(id=1)
        expected.name = TestData.get_action()
        expected.save()
        actual = Action.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = Action.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Action.DoesNotExist) as context:
            Action.objects.get(pk=expected.id)
        msg = 'Action matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Action()
        expected.name = self.action_data['name']
        expected.save()
        actual = Action.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestAgeModel(APITestCase):
    fixtures = ['age']

    def setUp(self):
        self.age_data = {'name': '10 years'}

    def tearDown(self):
        self.age_data = None

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))

    def test_01_object(self):
        a = Age()
        self.assertEqual("<class 'assets.models.Age'>",
                         repr(a))
        self.assertEqual("<class 'assets.models.Age'>",
                         str(a))
        a = Age.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Age'>:{}".format(a.id),
                         repr(a))
        self.assertEqual(a.name,
                         str(a))
 
    def test_02_get(self):
        a = Age.objects.get(id=1)
        self.assertEqual('1 year',
                         a.name)        

    def test_03_filter(self):
        expected = Age.objects.filter(name='1 year')
        actual = Age.objects.filter(name__endswith='year')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        a = Age.objects.create(**self.age_data)
        self.assertEqual(self.age_data['name'],
                         a.name)

    def test_05_full_update(self):
        expected = Age.objects.get(id=1)
        expected.name = TestData.get_random_age()
        expected.save()
        actual = Age.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = Age.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Age.DoesNotExist) as context:
            Age.objects.get(pk=expected.id)
        msg = 'Age matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Age()
        expected.name = self.age_data['name']
        expected.save()
        actual = Age.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestBreedModel(APITestCase):
    fixtures = ['breed']

    def setUp(self):
        self.breed_data = {'name': TestData.get_breed(),
                           'url': TestData.get_image()}

    def tearDown(self):
        self.breed_data = None

    def test_00_load_fixtures(self):
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))

    def test_01_object(self):
        b = Breed()
        self.assertEqual("<class 'assets.models.Breed'>",
                         repr(b))
        self.assertEqual("<class 'assets.models.Breed'>",
                         str(b))
        b = Breed.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Breed'>:{}".format(b.id),
                         repr(b))
        self.assertEqual(b.name,
                         str(b))
 
    def test_02_get(self):
        b = Breed.objects.get(id=1)
        self.assertEqual('Holstein',
                         b.name)        

    def test_03_filter(self):
        expected = Breed.objects.filter(name='Holstein')
        actual = Breed.objects.filter(name__endswith='ein')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        b = Breed.objects.create(**self.breed_data)
        self.assertEqual(self.breed_data['name'],
                         b.name)
        self.assertEqual(self.breed_data['url'],
                         b.url)

    def test_05_full_update(self):
        expected = Breed.objects.get(id=1)
        expected.name = TestData.get_random_breed()
        expected.url = TestData.get_random_image()
        expected.save()
        actual = Breed.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
        self.assertEqual(expected.url,
                         actual.url)
                             
    def test_06_delete(self):
        expected = Breed.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Breed.DoesNotExist) as context:
            Breed.objects.get(pk=expected.id)
        msg = 'Breed matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Breed()
        expected.name = self.breed_data['name']
        expected.url = self.breed_data['url']
        expected.save()
        actual = Breed.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
        self.assertEqual(expected.url,
                         actual.url)

class TestColorModel(APITestCase):
    fixtures = ['color']

    def setUp(self):
        self.color_data = {'name': 'blue'}

    def tearDown(self):
        self.color_data = None

    def test_00_load_fixtures(self):
        colors = Color.objects.all()
        self.assertEqual(9,
                         len(colors))

    def test_01_object(self):
        c = Color()
        self.assertEqual("<class 'assets.models.Color'>",
                         repr(c))
        self.assertEqual("<class 'assets.models.Color'>",
                         str(c))
        c = Color.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Color'>:{}".format(c.id),
                         repr(c))
        self.assertEqual(c.name,
                         str(c))
 
    def test_02_get(self):
        c = Color.objects.get(id=1)
        self.assertEqual('black_white',
                         c.name)        

    def test_03_filter(self):
        expected = Color.objects.filter(name='black_white')
        actual = Color.objects.filter(name__startswith='black')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        c = Color.objects.create(**self.color_data)
        self.assertEqual(self.color_data['name'],
                         c.name)

    def test_05_full_update(self):
        expected = Color.objects.get(id=1)
        expected.name = TestData.get_random_color()
        expected.save()
        actual = Color.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = Color.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Color.DoesNotExist) as context:
            Color.objects.get(pk=expected.id)
        msg = 'Color matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Color()
        expected.name = self.color_data['name']
        expected.save()
        actual = Color.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestCerealHayModel(APITestCase):
    fixtures = ['cerealhay']

    def setUp(self):
        self.cereal_data = {'name': TestData.get_cereal()}

    def tearDown(self):
        self.cereal_data = None

    def test_00_load_fixtures(self):
        cereal_hays = CerealHay.objects.all()
        self.assertEqual(5,
                         len(cereal_hays))

    def test_01_object(self):
        ch = CerealHay()
        self.assertEqual("<class 'assets.models.CerealHay'>",
                         repr(ch))
        self.assertEqual("<class 'assets.models.CerealHay'>",
                         str(ch))
        ch = CerealHay.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.CerealHay'>:{}".format(ch.id),
                         repr(ch))
        self.assertEqual(ch.name,
                         str(ch))
 
    def test_02_get(self):
        ch = CerealHay.objects.get(id=1)
        self.assertEqual('alfalfa',
                         ch.name)        

    def test_03_filter(self):
        expected = CerealHay.objects.filter(name='alfalfa')
        actual = CerealHay.objects.filter(name__endswith='fa')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        ch = CerealHay.objects.create(**self.cereal_data)
        self.assertEqual(self.cereal_data['name'],
                         ch.name)

    def test_05_full_update(self):
        expected = CerealHay.objects.get(id=1)
        expected.name = TestData.get_cereal()
        expected.save()
        actual = CerealHay.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = CerealHay.objects.get(id=1)
        expected.delete()
        with self.assertRaises(CerealHay.DoesNotExist) as context:
            CerealHay.objects.get(pk=expected.id)
        msg = 'CerealHay matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = CerealHay()
        expected.name = self.cereal_data['name']
        expected.save()
        actual = CerealHay.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestGrassHayModel(APITestCase):
    fixtures = ['grasshay']

    def setUp(self):
        self.grass_data = {'name': TestData.get_grass()}

    def tearDown(self):
        self.grass_data = None

    def test_00_load_fixtures(self):
        grass_hays = GrassHay.objects.all()
        self.assertEqual(9,
                         len(grass_hays))

    def test_01_object(self):
        gh = GrassHay()
        self.assertEqual("<class 'assets.models.GrassHay'>",
                         repr(gh))
        self.assertEqual("<class 'assets.models.GrassHay'>",
                         str(gh))
        gh = GrassHay.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.GrassHay'>:{}".format(gh.id),
                         repr(gh))
        self.assertEqual(gh.name,
                         str(gh))
 
    def test_02_get(self):
        gh = GrassHay.objects.get(id=1)
        self.assertEqual('bermuda',
                         gh.name)        

    def test_03_filter(self):
        expected = GrassHay.objects.filter(name='bermuda')
        actual = GrassHay.objects.filter(name__endswith='a')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        gh = GrassHay.objects.create(**self.grass_data)
        self.assertEqual(self.grass_data['name'],
                         gh.name)

    def test_05_full_update(self):
        expected = GrassHay.objects.get(id=1)
        expected.name = TestData.get_grass()
        expected.save()
        actual = GrassHay.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = GrassHay.objects.get(id=1)
        expected.delete()
        with self.assertRaises(GrassHay.DoesNotExist) as context:
            GrassHay.objects.get(pk=expected.id)
        msg = 'GrassHay matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = GrassHay()
        expected.name = self.grass_data['name']
        expected.save()
        actual = GrassHay.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestIllnessModel(APITestCase):
    fixtures = ['illness']

    def setUp(self):
        self.illness_data = {'diagnosis': TestData.get_illness()}

    def tearDown(self):
        self.illness_data = None

    def test_00_load_fixtures(self):
        illnesses = Illness.objects.all()
        self.assertEqual(15,
                         len(illnesses))

    def test_01_object(self):
        i = Illness()
        self.assertEqual("<class 'assets.models.Illness'>",
                         repr(i))
        self.assertEqual("<class 'assets.models.Illness'>",
                         str(i))
        i = Illness.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Illness'>:{}".format(i.id),
                         repr(i))
        self.assertEqual('{}: {}'.format(i.diagnosis, i.treatment),
                         str(i))
 
    def test_02_get(self):
        i = Illness.objects.get(id=1)
        self.assertEqual('fever',
                         i.diagnosis)

    def test_03_filter(self):
        expected = Illness.objects.filter(diagnosis='infection')
        actual = Illness.objects.filter(diagnosis__endswith='tion')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        i = Illness.objects.create(**self.illness_data)
        self.assertEqual(self.illness_data['diagnosis'],
                         i.diagnosis)

    def test_05_full_update(self):
        expected = Illness.objects.get(id=1)
        expected.diagnosis = TestData.get_illness()
        expected.save()
        actual = Illness.objects.get(id=expected.id)
        self.assertEqual(expected.diagnosis,
                         actual.diagnosis)
                             
    def test_06_delete(self):
        expected = Illness.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Illness.DoesNotExist) as context:
            Illness.objects.get(pk=expected.id)
        msg = 'Illness matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Illness()
        expected.name = self.illness_data['diagnosis']
        expected.save()
        actual = Illness.objects.get(pk=expected.id)
        self.assertEqual(expected.diagnosis,
                         actual.diagnosis)

class TestInjuryModel(APITestCase):
    fixtures = ['injury']

    def setUp(self):
        self.injury_data = {'diagnosis': TestData.get_injury()}

    def tearDown(self):
        self.injury_data = None

    def test_00_load_fixtures(self):
        injuries = Injury.objects.all()
        self.assertEqual(5,
                         len(injuries))

    def test_01_object(self):
        i = Injury()
        self.assertEqual("<class 'assets.models.Injury'>",
                         repr(i))
        self.assertEqual("<class 'assets.models.Injury'>",
                         str(i))
        i = Injury.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Injury'>:{}".format(i.id),
                         repr(i))
        self.assertEqual('{}: {}'.format(i.diagnosis, i.treatment),
                         str(i))
 
    def test_02_get(self):
        i = Injury.objects.get(id=1)
        self.assertEqual('chapped teat',
                         i.diagnosis)

    def test_03_filter(self):
        expected = Injury.objects.filter(diagnosis='sprain')
        actual = Injury.objects.filter(diagnosis__endswith='in')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        i = Injury.objects.create(**self.injury_data)
        self.assertEqual(self.injury_data['diagnosis'],
                         i.diagnosis)

    def test_05_full_update(self):
        expected = Injury.objects.get(id=1)
        expected.diagnosis = TestData.get_injury()
        expected.save()
        actual = Injury.objects.get(id=expected.id)
        self.assertEqual(expected.diagnosis,
                         actual.diagnosis)
                             
    def test_06_delete(self):
        expected = Injury.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Injury.DoesNotExist) as context:
            Injury.objects.get(pk=expected.id)
        msg = 'Injury matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Injury()
        expected.name = self.injury_data['diagnosis']
        expected.save()
        actual = Injury.objects.get(pk=expected.id)
        self.assertEqual(expected.diagnosis,
                         actual.diagnosis)

class TestLegumeHayModel(APITestCase):
    fixtures = ['legumehay']

    def setUp(self):
        self.legume_data = {'name': TestData.get_legume()}

    def tearDown(self):
        self.legume_data = None

    def test_00_load_fixtures(self):
        legume_hays = LegumeHay.objects.all()
        self.assertEqual(6,
                         len(legume_hays))

    def test_01_object(self):
        lh = LegumeHay()
        self.assertEqual("<class 'assets.models.LegumeHay'>",
                         repr(lh))
        self.assertEqual("<class 'assets.models.LegumeHay'>",
                         str(lh))
        lh = LegumeHay.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.LegumeHay'>:{}".format(lh.id),
                         repr(lh))
        self.assertEqual(lh.name,
                         str(lh))
 
    def test_02_get(self):
        lh = LegumeHay.objects.get(id=1)
        self.assertEqual('clover',
                         lh.name)        

    def test_03_filter(self):
        expected = LegumeHay.objects.filter(name=TestData.get_legume())
        actual = LegumeHay.objects.filter(name__endswith='foin')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        lh = LegumeHay.objects.create(**self.legume_data)
        self.assertEqual(self.legume_data['name'],
                         lh.name)

    def test_05_full_update(self):
        expected = LegumeHay.objects.get(id=1)
        expected.name = TestData.get_legume()
        expected.save()
        actual = LegumeHay.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = LegumeHay.objects.get(id=1)
        expected.delete()
        with self.assertRaises(LegumeHay.DoesNotExist) as context:
            LegumeHay.objects.get(pk=expected.id)
        msg = 'LegumeHay matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = LegumeHay()
        expected.name = self.legume_data['name']
        expected.save()
        actual = LegumeHay.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestPastureModel(APITestCase):
    fixtures = ['pasture']

    def setUp(self):
        self.pasture_data = {'name': TestData.get_pasture(),
                            'url': TestData.get_pastureimage(),
                            'fallow': False,
                            'distance': randint(1, 5)}

    def tearDown(self):
        self.pasture_data = None

    def test_00_load_fixtures(self):
        pastures = Pasture.objects.all()
        self.assertEqual(13,
                         len(pastures))

    def test_01_object(self):
        p = Pasture()
        self.assertEqual("<class 'assets.models.Pasture'>",
                         repr(p))
        self.assertEqual("<class 'assets.models.Pasture'>",
                         str(p))
        p = Pasture.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Pasture'>:{}".format(p.id),
                         repr(p))
        self.assertEqual(p.name,
                         str(p))
 
    def test_02_get(self):
        p = Pasture.objects.get(id=1)
        self.assertEqual('North',
                         p.name)
        self.assertEqual('/static/images/regions/north.png',
                         p.url)
        self.assertFalse(p.fallow)
        self.assertLessEqual(1,
                             p.distance)

    def test_03_filter(self):
        expected = Pasture.objects.filter(name='Pen')
        actual = Pasture.objects.filter(name__endswith='en')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        p = Pasture.objects.create(**self.pasture_data)
        self.assertEqual(self.pasture_data['name'],
                         p.name)
        self.assertEqual(self.pasture_data['url'],
                         p.url)

    def test_05_full_update(self):
        expected = Pasture.objects.get(id=1)
        expected.name = TestData.get_pasture()
        expected.save()
        actual = Pasture.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
        self.assertEqual(expected.url,
                         actual.url)
        self.assertEqual(expected.fallow,
                         actual.fallow)
        self.assertEqual(expected.distance,
                         actual.distance)
                             
    def test_06_delete(self):
        expected = Pasture.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Pasture.DoesNotExist) as context:
            Pasture.objects.get(pk=expected.id)
        msg = 'Pasture matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Pasture()
        expected.name = self.pasture_data['name']
        expected.url = self.pasture_data['url']
        expected.fallow = self.pasture_data['fallow']
        expected.distance = self.pasture_data['distance']
        expected.save()
        actual = Pasture.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
        self.assertEqual(expected.url,
                         actual.url)
        self.assertEqual(expected.fallow,
                         actual.fallow)
        self.assertEqual(expected.distance,
                         actual.distance)

class TestSeasonModel(APITestCase):
    fixtures = ['season']

    def setUp(self):
        self.season_data = {'name': TestData.get_season()}

    def tearDown(self):
        self.season_data = None

    def test_00_load_fixtures(self):
        seasons = Season.objects.all()
        self.assertEqual(4,
                         len(seasons))

    def test_01_object(self):
        s = Season()
        self.assertEqual("<class 'assets.models.Season'>",
                         repr(s))
        self.assertEqual("<class 'assets.models.Season'>",
                         str(s))
        s = Season.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Season'>:{}".format(s.id),
                         repr(s))
        self.assertEqual(s.name,
                         str(s))
 
    def test_02_get(self):
        s = Season.objects.get(id=1)
        self.assertEqual('Spring',
                         s.name)        

    def test_03_filter(self):
        expected = Season.objects.filter(name='Spring')
        actual = Season.objects.filter(name__endswith='ng')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        self.season_data.update({'name': 'Fall'})
        s = Season.objects.create(**self.season_data)
        self.assertEqual('Fall',
                         s.name)

    def test_05_full_update(self):
        expected = Season.objects.get(id=4)
        expected.name = 'Old Man Winter'
        expected.save()
        actual = Season.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = Season.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Season.DoesNotExist) as context:
            Season.objects.get(pk=expected.id)
        msg = 'Season matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Season()
        expected.name = 'Fall'
        expected.save()
        actual = Season.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestStatusModel(APITestCase):
    fixtures = ['status']

    def setUp(self):
        self.status_data = {'name': TestData.get_status()}

    def tearDown(self):
        self.status_data = None

    def test_00_load_fixtures(self):
        statuses = Status.objects.all()
        self.assertEqual(5,
                         len(statuses))

    def test_01_object(self):
        s = Status()
        self.assertEqual("<class 'assets.models.Status'>",
                         repr(s))
        self.assertEqual("<class 'assets.models.Status'>",
                         str(s))
        s = Status.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Status'>:{}".format(s.id),
                         repr(s))
        self.assertEqual(s.name,
                         str(s))
 
    def test_02_get(self):
        s = Status.objects.get(id=1)
        self.assertEqual('Healthy',
                         s.name)        

    def test_03_filter(self):
        expected = Status.objects.filter(name='Pregnant')
        actual = Status.objects.filter(name__endswith='nt')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        s = Status.objects.create(**self.status_data)
        self.assertEqual(self.status_data['name'],
                         s.name)

    def test_05_full_update(self):
        expected = Status.objects.get(id=1)
        expected.name = TestData.get_status()
        expected.save()
        actual = Status.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = Status.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Status.DoesNotExist) as context:
            Status.objects.get(pk=expected.id)
        msg = 'Status matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Status()
        expected.name = self.status_data['name']
        expected.save()
        actual = Status.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TTestTreatmentModel(APITestCase):
    fixtures = ['treatment']

    def setUp(self):
        self.treatment_data = {'name': TestData.get_treatment()}

    def tearDown(self):
        self.treatment_data = None

    def test_00_load_fixtures(self):
        treatments = Treatment.objects.all()
        self.assertEqual(14,
                         len(treatments))

    def test_01_object(self):
        t = Treatment()
        self.assertEqual("<class 'assets.models.Treatment'>",
                         repr(t))
        self.assertEqual("<class 'assets.models.Treatment'>",
                         str(t))
        t = Treatment.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Treatment'>:{}".format(t.id),
                         repr(t))
        self.assertEqual(t.name,
                         str(t))
 
    def test_02_get(self):
        t = Treatment.objects.get(id=1)
        self.assertEqual('apply salve',
                         t.name)        

    def test_03_filter(self):
        expected = Treatment.objects.filter(name='pedicure')
        actual = Treatment.objects.filter(name__endswith='re')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        t = Treatment.objects.create(**self.treatment_data)
        self.assertEqual(self.treatment_data['name'],
                         t.name)

    def test_05_full_update(self):
        expected = Treatment.objects.get(id=1)
        expected.name = TestData.get_treatment()
        expected.save()
        actual = Treatment.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = Treatment.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Treatment.DoesNotExist) as context:
            Treatment.objects.get(pk=expected.id)
        msg = 'Treatment matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Treatment()
        expected.name = self.treatment_data['name']
        expected.save()
        actual = Treatment.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TTestVaccineModel(APITestCase):
    fixtures = ['vaccine']

    def setUp(self):
        self.vaccine_data = {'name': TestData.get_vaccine()}

    def tearDown(self):
        self.vaccine_data = None

    def test_00_load_fixtures(self):
        vaccines = Vaccine.objects.all()
        self.assertEqual(6,
                         len(vaccines))

    def test_01_object(self):
        v = Vaccine()
        self.assertEqual("<class 'assets.models.Vaccine'>",
                         repr(v))
        self.assertEqual("<class 'assets.models.Vaccine'>",
                         str(v))
        v = Vaccine.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Vaccine'>:{}".format(v.id),
                         repr(v))
        self.assertEqual(v.name,
                         str(v))
 
    def test_02_get(self):
        v = Vaccine.objects.get(id=1)
        self.assertEqual('BRD vaccine',
                         v.name)        

    def test_03_filter(self):
        expected = Vaccine.objects.filter(name='ketosis vaccine')
        actual = Vaccine.objects.filter(name__startswith='ket')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        v = Vaccine.objects.create(**self.vaccine_data)
        self.assertEqual(self.vaccine_data['name'],
                         v.name)

    def test_05_full_update(self):
        expected = Vaccine.objects.get(id=1)
        expected.name = TestData.get_vaccine()
        expected.save()
        actual = Vaccine.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_06_delete(self):
        expected = Vaccine.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Vaccine.DoesNotExist) as context:
            Vaccine.objects.get(pk=expected.id)
        msg = 'Vaccine matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Vaccine()
        expected.name = self.vaccine_data['name']
        expected.save()
        actual = Vaccine.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TTestCowModel(APITestCase):
    fixtures = ['age', 'breed', 'color', 'user', 'cow']

    def setUp(self):
        self.rfid = TestData.get_rfid()
        self.age_data = {'name': '10 years'}
        self.breed_data = {'name': TestData.get_breed(),
                           'url': TestData.get_image()}
        self.color_data = {'name': 'blue'}
        self.cow_data = {'purchased_by': User.objects.get(username=TestData.get_random_user()),
                         'purchase_date': TestTime.get_date()}

    def tearDown(self):
        self.rfid = None
        self.age_data = None
        self.breed_data = None
        self.color_data = None

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        colors = Color.objects.all()
        self.assertEqual(9,
                         len(colors))
        cows = Cow.objects.all()
        self.assertEqual(130,
                         len(cows))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        cows = Cow.objects.all()
        self.assertLessEqual(10,
                             len(cows))

    def test_01_object(self):
        c = Cow()
        self.assertEqual("<class 'assets.models.Cow'>",
                         repr(c))
        self.assertEqual("<class 'assets.models.Cow'>",
                         str(c))
        c = Cow.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Cow'>:{}".format(c.rfid),
                         repr(c))
        self.assertEqual(str(c.rfid),
                         str(c))
 
    def test_02_get(self):
        c = Cow.objects.get(id=1)
        self.assertRegex(str(c.rfid),
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertRegex(c.age.name,
                         ' year')
        self.assertRegex(c.color.name,
                         '_white$')
        self.assertRegex(c.breed.name,
                         'Holstein')
        self.assertRegex(c.breed.url,
                         '/holstein.png$')
        self.assertEqual(TestTime.get_purchase_date(),
                         TestTime.convert_date(c.purchase_date))
        self.assertEqual(TestData.get_random_user(),
                         c.purchased_by.username)

    def test_03_filter(self):
        expected = Cow.objects.filter(breed__url='/static/images/breeds/holstein.png')
        actual = Cow.objects.filter(breed__url__endswith='holstein.png')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        a = Age.objects.create(**self.age_data)
        b = Breed.objects.create(**self.breed_data)
        c = Color.objects.create(**self.color_data)
        self.cow_data.update({'rfid': self.rfid,
                              'age': a,
                              'breed': b,
                              'color': c})
        actual = Cow.objects.create(**self.cow_data)
        self.assertRegex(str(actual.rfid),
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertEqual(self.age_data['name'],
                         actual.age.name)
        self.assertEqual(self.breed_data['name'],
                         actual.breed.name)
        self.assertEqual(self.breed_data['url'],
                         actual.breed.url)
        self.assertEqual(self.color_data['name'],
                         actual.color.name)
        self.assertEqual(self.cow_data['purchase_date'],
                         actual.purchase_date)
        self.assertEqual(self.cow_data['purchased_by'],
                         actual.purchased_by)

    def test_05_full_update(self):
        a = Age.objects.create(**self.age_data)
        b = Breed.objects.create(**self.breed_data)
        c = Color.objects.create(**self.color_data)
        u = User.objects.get(username=TestData.get_random_user())
        d = TestTime.get_date()
        expected = Cow.objects.get(id=1)
        expected.age = a
        expected.breed = b
        expected.color = c
        expected.purchased_by = u
        expected.purchase_date = d
        expected.save()
        actual = Cow.objects.get(id=expected.id)
        self.assertRegex(str(actual.rfid),
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertEqual(expected.age.name,
                         actual.age.name)
        self.assertEqual(expected.color.name,
                         actual.color.name)
        self.assertEqual(expected.breed.name,
                         actual.breed.name)
        self.assertEqual(expected.breed.url,
                         actual.breed.url)
                             
    def test_06_partial_update(self):
        a = Age.objects.create(**self.age_data)
        expected = Cow.objects.get(id=1)
        expected.age = a
        expected.save()
        actual = Cow.objects.get(id=expected.id)
        self.assertEqual(expected.age.name,
                         actual.age.name)

    def test_07_delete(self):
        expected = Cow.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Cow.DoesNotExist) as context:
            Cow.objects.get(pk=expected.id)
        msg = 'Cow matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_08_save(self):
        a = Age.objects.create(**self.age_data)
        b = Breed.objects.create(**self.breed_data)
        c = Color.objects.create(**self.color_data)
        u = User.objects.get(username=TestData.get_random_user())
        expected = Cow()
        expected.rfid = self.rfid
        expected.age = a
        expected.breed = b 
        expected.color = c
        expected.purchased_by = u
        expected.purchase_date = TestTime.get_purchase_date()
        expected.save()
        actual = Cow.objects.get(pk=expected.id)
        self.assertRegex(str(actual.rfid),
                         '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$')
        self.assertEqual(expected.age.name,
                         actual.age.name)
        self.assertEqual(expected.color.name,
                         actual.color.name)
        self.assertEqual(expected.breed.name,
                         actual.breed.name)
        self.assertEqual(expected.breed.url,
                         actual.breed.url)

class TestSeedModel(APITestCase):
    # Note: loading order does matter
    fixtures = ['cerealhay', 'grasshay', 'legumehay', 'season',
                'user', 'pasture', 'seed']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        region = Region.objects.get(pk=11)
        season = Season.objects.get(name=TestData.get_season())
        cereal_data = {'name': TestData.get_cereal()}
        cereal = CerealHay.objects.create(**cereal_data)
        grass_data = {'name': TestData.get_grass()}
        grass = GrassHay.objects.create(**grass_data)
        legume_data = {'name': TestData.get_legume()}
        legume = LegumeHay.objects.create(**legume_data)
        self.pasture_data = {'seeded_by': user,
                             'year': TestTime.get_year(),
                             'season': season,
                             'region': region,
                             'cereal_hay': cereal,
                             'grass_hay': grass,
                             'legume_hay': legume}

    def tearDown(self):
        self.pasture_data = None

    def test_00_load_fixtures(self):
        cereals = CerealHay.objects.all()
        self.assertEqual(6,
                         len(cereals))
        grasses = GrassHay.objects.all()
        self.assertEqual(10,
                         len(grasses))
        legumes = LegumeHay.objects.all()
        self.assertEqual(7,
                         len(legumes))
        regions = Region.objects.all()
        self.assertEqual(13,
                         len(regions))
        seasons = Season.objects.all()
        self.assertEqual(4,
                         len(seasons))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        pastures = Pasture.objects.all()
        self.assertEqual(13,
                         len(pastures))

    def test_01_object(self):
        p = Pasture()
        self.assertEqual("<class 'assets.models.Pasture'>",
                         repr(p))
        self.assertEqual("<class 'assets.models.Pasture'>",
                         str(p))
        p = Pasture.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Pasture'>:{}".format(p.id),
                         repr(p))
        self.assertEqual(p.region.name,
                         str(p))
 
    def test_02_get(self):
        p = Pasture.objects.get(id=1)
        self.assertEqual(TestData.get_random_user(),
                         p.seeded_by.username)        
        self.assertEqual(2015,
                         p.year)
        self.assertRegex(p.season.name,
                         '\w+')
        self.assertEqual('North',
                         p.region.name)        
        self.assertEqual('/static/images/regions/north.png',
                         p.region.url)        
        self.assertEqual('alfalfa',
                         p.cereal_hay.name)        
        self.assertEqual('bermuda',
                         p.grass_hay.name)        
        self.assertEqual('clover',
                         p.legume_hay.name)        

    def test_03_filter(self):
        expected = Pasture.objects.filter(region__name=TestData.get_pasture())
        actual = Pasture.objects.filter(region__name__endswith='ll')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        p = Pasture.objects.create(**self.pasture_data)
        actual = Pasture.objects.get(pk=p.id)
        self.assertEqual(p.seeded_by.username,
                         actual.seeded_by.username)
        self.assertEqual(p.year,
                         actual.year)
        self.assertEqual(p.season.name,
                         actual.season.name)        
        self.assertEqual(p.region.name,
                         actual.region.name)        
        self.assertEqual(p.region.url,
                         actual.region.url)        
        self.assertEqual(p.cereal_hay.name,
                         actual.cereal_hay.name)        
        self.assertEqual(p.grass_hay.name,
                         actual.grass_hay.name)        
        self.assertEqual(p.legume_hay.name,
                         actual.legume_hay.name)        

    def test_05_full_update(self):
        expected = Pasture.objects.get(id=1)
        expected.seeded_by = self.pasture_data['seeded_by']
        expected.region = self.pasture_data['region']
        expected.cereal_hay = self.pasture_data['cereal_hay']
        expected.grass_hay = self.pasture_data['grass_hay']
        expected.legume_hay = self.pasture_data['legume_hay']
        expected.save()
        actual = Pasture.objects.get(id=expected.id)
        self.assertEqual(expected.seeded_by.username,
                         actual.seeded_by.username)
        self.assertEqual(expected.year,
                         actual.year)
        self.assertEqual(expected.season.name,
                         actual.season.name)
        self.assertEqual(expected.region.name,
                         actual.region.name)        
        self.assertEqual(expected.region.url,
                         actual.region.url)        
        self.assertEqual(expected.cereal_hay.name,
                         actual.cereal_hay.name)        
        self.assertEqual(expected.grass_hay.name,
                         actual.grass_hay.name)        
        self.assertEqual(expected.legume_hay.name,
                         actual.legume_hay.name)        
                             
    def test_06_delete(self):
        expected = Pasture.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Pasture.DoesNotExist) as context:
            Pasture.objects.get(pk=expected.id)
        msg = 'Pasture matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Pasture()
        expected.seeded_by = self.pasture_data['seeded_by']
        expected.year = self.pasture_data['year']
        expected.season = Season.objects.get(name='Spring')
        expected.region = Region.objects.get(name='North')
        expected.cereal_hay = self.pasture_data['cereal_hay']
        expected.grass_hay = self.pasture_data['grass_hay']
        expected.legume_hay = self.pasture_data['legume_hay']
        expected.save()
        actual = Pasture.objects.get(pk=expected.id)
        self.assertEqual(expected.seeded_by.username,
                         actual.seeded_by.username)
        self.assertEqual(expected.year,
                         actual.year)
        self.assertEqual(expected.season.name,
                         actual.season.name)
        self.assertEqual(expected.region.name,
                         actual.region.name)        
        self.assertEqual(expected.region.url,
                         actual.region.url)        
        self.assertEqual(expected.cereal_hay.name,
                         actual.cereal_hay.name)        
        self.assertEqual(expected.grass_hay.name,
                         actual.grass_hay.name)        
        self.assertEqual(expected.legume_hay.name,
                         actual.legume_hay.name)        

class TTestEventModel(APITestCase):
    # Note: loading order does matter
    fixtures = ['action', 'age', 'breed', 'color', 'cow', 'user', 'event']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        action = Action.objects.get(pk=1)
        cow = Cow.objects.get(pk=1)
        self.event_data = {'recorded_by': user,
                           'cow': cow,
                           'action': action}

    def tearDown(self):
        self.event_data = None

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        colors = Color.objects.all()
        self.assertEqual(9,
                         len(colors))
        cows = Cow.objects.all()
        self.assertEqual(130,
                         len(cows))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        events = Event.objects.all()
        self.assertLessEqual(10,
                             len(events))

    def test_01_object(self):
        e = Event()
        self.assertEqual("<class 'assets.models.Event'>",
                         repr(e))
        self.assertEqual("<class 'assets.models.Event'>",
                         str(e))
        e = Event.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Event'>:{}".format(e.id),
                         repr(e))
        # ie. vet: 2018-02-09 19:03:16.019000+00:00: 1 year: red_white: Holstein: Wake Up
        (user, date, time, tmp) = str(e).split(' ', 3)
        self.assertEqual('{}:'.format(e.recorded_by.username),
                         user)
        self.assertRegex(date,
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(time,
                         '^\d{2}:\d{2}:\d{2}.\d{6}\+\d{2}:\d{2}:$')
        (rfid, action_name) = tmp.split(':')
        self.assertEqual(str(e.cow.rfid),
                         rfid.strip())
        self.assertEqual(e.action.name,
                         action_name.strip())
 
    def test_02_get(self):
        e = Event.objects.get(id=1)
        self.assertEqual('vet',
                         e.recorded_by.username)        
        self.assertEqual('Holstein',
                         e.cow.breed.name)        
        self.assertEqual('Wake Up',
                         e.action.name)        

    def test_03_filter(self):
        expected = Event.objects.filter(cow__breed__name='Holstein')
        actual = Event.objects.filter(cow__breed__name__endswith='ein')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        e = Event.objects.create(**self.event_data)
        actual = Event.objects.get(pk=e.id)
        self.assertEqual(e.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(e.cow.age.name,
                         actual.cow.age.name)        
        self.assertEqual(e.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(e.cow.breed.url,
                         actual.cow.breed.url)        
        self.assertEqual(e.cow.color.name,
                         actual.cow.color.name)        
        self.assertEqual(e.action.name,
                         actual.action.name)        

    def test_05_full_update(self):
        expected = Event.objects.get(id=1)
        expected.recorded_by = self.event_data['recorded_by']
        expected.cow = self.event_data['cow']
        expected.action = self.event_data['action']
        expected.save()
        actual = Event.objects.get(id=expected.id)
        self.assertEqual(expected.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(expected.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(expected.action.name,
                         actual.action.name)        
                             
    def test_06_delete(self):
        expected = Event.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Event.DoesNotExist) as context:
            Event.objects.get(pk=expected.id)
        msg = 'Event matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Event()
        expected.recorded_by = self.event_data['recorded_by']
        expected.cow = self.event_data['cow']
        expected.action = self.event_data['action']
        expected.save()
        actual = Event.objects.get(pk=expected.id)
        self.assertEqual(expected.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(expected.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(expected.action.name,
                         actual.action.name)        

class TTestExerciseModel(APITestCase):
    # Note: loading order does matter
    fixtures = ['age', 'breed', 'cerealhay', 'color', 'grasshay',
                'legumehay', 'region', 'user', 'cow', 'season',
                'pasture', 'exercise']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        cow = Cow.objects.get(pk=1)
        pasture = Pasture.objects.get(pk=1)
        distance = 1
        self.exercise_data = {'recorded_by': user,
                              'cow': cow,
                              'pasture': pasture,
                              'distance': distance}

    def tearDown(self):
        self.exercise_data = None

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        cereals = CerealHay.objects.all()
        self.assertEqual(5,
                         len(cereals))
        colors = Color.objects.all()
        self.assertEqual(9,
                         len(colors))
        grasses = GrassHay.objects.all()
        self.assertEqual(9,
                         len(grasses))
        legumes = LegumeHay.objects.all()
        self.assertEqual(6,
                         len(legumes))
        regions = Region.objects.all()
        self.assertEqual(13,
                         len(regions))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        cows = Cow.objects.all()
        self.assertEqual(130,
                         len(cows))
        pastures = Pasture.objects.all()
        self.assertEqual(13,
                         len(pastures))
        exercises = Exercise.objects.all()
        self.assertLessEqual(10,
                             len(exercises))

    def test_01_object(self):
        e = Exercise()
        self.assertEqual("<class 'assets.models.Exercise'>",
                         repr(e))
        self.assertEqual("<class 'assets.models.Exercise'>",
                         str(e))
        e = Exercise.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Exercise'>:{}".format(e.id),
                         repr(e))
        # ie. vet: 2018-02-09 20:55:09.735000+00:00: 3 years: black_white: Holstein: Central North
        (user, date, time, tmp) = str(e).split(' ', 3)
        self.assertEqual('{}:'.format(e.recorded_by.username),
                         user)
        self.assertRegex(date,
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(time,
                         '^\d{2}:\d{2}:\d{2}.\d{6}\+\d{2}:\d{2}:$')
        (age, breed, color, pasture_name, distance) = tmp.split(':')
        self.assertEqual(e.cow.age.name,
                         age.strip())
        self.assertEqual(e.cow.breed.name,
                         breed.strip())
        self.assertEqual(e.cow.color.name,
                         color.strip())
        self.assertEqual(e.pasture.region.name,
                         pasture_name.strip())
        self.assertEqual(e.distance,
                         int(distance.strip()))
 
    def test_02_get(self):
        e = Exercise.objects.get(id=1)
        self.assertEqual('vet',
                         e.recorded_by.username)        
        self.assertEqual('Holstein',
                         e.cow.breed.name)        
        self.assertRegex(e.pasture.region.name,
                         '\w{2}')
        self.assertLessEqual(1,
                             e.distance)        

    def test_03_filter(self):
        expected = Exercise.objects.filter(pasture__region__name='Central North')
        actual = Exercise.objects.filter(pasture__region__name__endswith='rth')
        self.assertLessEqual(len(expected),
                             len(actual))

    def test_04_create(self):
        e = Exercise.objects.create(**self.exercise_data)
        actual = Exercise.objects.get(pk=e.id)
        self.assertEqual(e.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(e.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(e.pasture.region.name,
                         actual.pasture.region.name)        
        self.assertEqual(e.distance,
                         actual.distance)

    def test_05_full_update(self):
        expected = Exercise.objects.get(id=1)
        expected.recorded_by = self.exercise_data['recorded_by']
        expected.cow = self.exercise_data['cow']
        expected.pasture = self.exercise_data['pasture']
        expected.distance = self.exercise_data['distance']
        expected.save()
        actual = Exercise.objects.get(id=expected.id)
        self.assertEqual(expected.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(expected.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(expected.pasture.region.name,
                         actual.pasture.region.name)        
        self.assertEqual(expected.distance,
                         actual.distance)
                             
    def test_06_delete(self):
        expected = Exercise.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Exercise.DoesNotExist) as context:
            Exercise.objects.get(pk=expected.id)
        msg = 'Exercise matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Exercise()
        expected.recorded_by = self.exercise_data['recorded_by']
        expected.cow = self.exercise_data['cow']
        expected.pasture = self.exercise_data['pasture']
        expected.distance = self.exercise_data['distance']
        expected.save()
        actual = Exercise.objects.get(pk=expected.id)
        self.assertEqual(expected.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(expected.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(expected.pasture.region.name,
                         actual.pasture.region.name)        

class TTestMilkModel(APITestCase):
    # Note: loading order does matter
    fixtures = ['age', 'breed', 'color', 'cow', 'user', 'milk']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        cow = Cow.objects.get(pk=1)
        gallons = 1
        self.milk_data = {'recorded_by': user,
                          'cow': cow,
                          'gallons': gallons}

    def tearDown(self):
        self.milk_data = None

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        colors = Color.objects.all()
        self.assertEqual(9,
                         len(colors))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))
        cows = Cow.objects.all()
        self.assertEqual(130,
                         len(cows))
        milk = Milk.objects.all()
        self.assertLessEqual(10,
                             len(milk))

    def test_01_object(self):
        m = Milk()
        self.assertEqual("<class 'assets.models.Milk'>",
                         repr(m))
        self.assertEqual("<class 'assets.models.Milk'>",
                         str(m))
        m = Milk.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.Milk'>:{}".format(m.id),
                         repr(m))
        # ie. vet: 2018-02-09 21:50:20.011000+00:00: 1 year: Holstein: red_white: 6
        (user, date, time, tmp) = str(m).split(' ', 3)
        self.assertEqual('{}:'.format(m.recorded_by.username),
                         user)
        self.assertRegex(date,
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(time,
                         '^\d{2}:\d{2}:\d{2}.\d{6}\+\d{2}:\d{2}:$')
        (age, breed, color, gallons) = tmp.split(':')
        self.assertEqual(m.cow.age.name,
                         age.strip())
        self.assertEqual(m.cow.color.name,
                         color.strip())
        self.assertEqual(m.cow.breed.name,
                         breed.strip())
        self.assertEqual('{}'.format(m.gallons),
                         gallons.strip())
 
    def test_02_get(self):
        m = Milk.objects.get(id=1)
        self.assertEqual('vet',
                         m.recorded_by.username)        
        self.assertEqual('Holstein',
                         m.cow.breed.name)        
        self.assertLessEqual(0,
                             m.gallons)

    def test_03_filter(self):
        expected = Milk.objects.filter(cow__breed__name='Holstein')
        actual = Milk.objects.filter(cow__breed__name__endswith='ein')
        self.assertLessEqual(len(expected),
                             len(actual))

    def test_04_create(self):
        m = Milk.objects.create(**self.milk_data)
        actual = Milk.objects.get(pk=m.id)
        self.assertEqual(m.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(m.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(m.gallons,
                         actual.gallons)

    def test_05_full_update(self):
        expected = Milk.objects.get(id=1)
        expected.recorded_by = self.milk_data['recorded_by']
        expected.cow = self.milk_data['cow']
        expected.gallons = self.milk_data['gallons']
        expected.save()
        actual = Milk.objects.get(id=expected.id)
        self.assertEqual(expected.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(expected.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(expected.gallons,
                         actual.gallons)
                             
    def test_06_delete(self):
        expected = Milk.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Milk.DoesNotExist) as context:
            Milk.objects.get(pk=expected.id)
        msg = 'Milk matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Milk()
        expected.recorded_by = self.milk_data['recorded_by']
        expected.cow = self.milk_data['cow']
        expected.gallons = self.milk_data['gallons']
        expected.save()
        actual = Milk.objects.get(pk=expected.id)
        self.assertEqual(expected.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(expected.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertEqual(expected.gallons,
                         actual.gallons)

class TTestHealthRecordModel(APITestCase):
    # Note: loading order does matter
    fixtures = ['age', 'breed', 'color', 'illness', 'injury',
                'status', 'vaccine', 'user', 'cow', 'healthrecord']

    def setUp(self):
        user = User.objects.get(username=TestData.get_random_user())
        cow = Cow.objects.get(pk=1)
        status = Status.objects.get(name='Healthy')
        illness = None
        injury = None
        vaccine = None
        self.hr_data = {'recorded_by': user,
                        'cow': cow,
                        'temperature': TestData.get_temp(),
                        'respiratory_rate': TestData.get_resp(),
                        'heart_rate': TestData.get_hr(),
                        'blood_pressure': TestData.get_bp(),
                        'weight': TestData.get_weight(),
                        'body_condition_score': TestData.get_bcs(),
                        'status': status}

    def tearDown(self):
        self.hr_data = None

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        colors = Color.objects.all()
        self.assertEqual(9,
                         len(colors))
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
        cows = Cow.objects.all()
        self.assertEqual(130,
                         len(cows))
        hr = HealthRecord.objects.all()
        self.assertLessEqual(10,
                             len(hr))

    def test_01_object(self):
        hr = HealthRecord()
        self.assertEqual("<class 'assets.models.HealthRecord'>",
                         repr(hr))
        self.assertEqual("<class 'assets.models.HealthRecord'>",
                         str(hr))
        hr = HealthRecord.objects.get(pk=1)
        self.assertEqual("<class 'assets.models.HealthRecord'>:{}".format(hr.id),
                         repr(hr))
        # ie. vet: 2015-01-01 04:00:00+00:00: 1 year, red_white, Holstein, 1, 100.8, 43.4, 67.2, 132.0, 490, 3.2, Healthy, 1
        (user, date, time, tmp) = str(hr).split(' ', 3)
        self.assertEqual('{}:'.format(hr.recorded_by.username),
                         user)
        self.assertRegex(date,
                         '^\d{4}-\d{2}-\d{2}$')
        if time.find('.') > 0:
            self.assertRegex(time,
                             '^\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}:$')
        else:
            self.assertRegex(time,
                             '^\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}:$')
        (age, breed, color, temp, resp, HR, BP, weight, BCS, status) = tmp.split(':')
        self.assertRegex(age.strip(), '\d year')
        self.assertRegex(breed.strip().lower(), '\w')
        self.assertRegex(color.strip(), '\w_\w')
        self.assertRegex(temp.strip(), '\d{3}\.\d')
        self.assertRegex(resp.strip(), '\d{2}\.\d')
        self.assertRegex(HR.strip(), '\d{2}\.\d')
        self.assertRegex(BP.strip(), '\d{3}\.\d')
        self.assertRegex(weight.strip(), '\d{3}')
        self.assertRegex(BCS.strip(), '\d\.\d')
        self.assertRegex(status.strip(), '\w')
        #self.assertRegex(treatment.strip(), '\w')
 
    def test_02_get(self):
        hr = HealthRecord.objects.get(id=1)
        self.assertRegex(hr.recorded_by.username, '\w')
        self.assertRegex(hr.cow.breed.name, '\w')
        self.assertIsInstance(hr.temperature, float)
        self.assertIsInstance(hr.respiratory_rate, float)
        self.assertIsInstance(hr.heart_rate, float)
        self.assertIsInstance(hr.blood_pressure, float)
        self.assertIsInstance(hr.weight, int)
        self.assertIsInstance(hr.body_condition_score, float)
        self.assertRegex(hr.status.name, '\w')
        self.assertGreaterEqual(hr.id, 0)

    def test_03_filter(self):
        expected = HealthRecord.objects.filter(cow__breed__name='Holstein')
        actual = HealthRecord.objects.filter(cow__breed__url__endswith='ein.png')
        self.assertLessEqual(len(expected),
                             len(actual))

    def test_04_create(self):
        hr = HealthRecord.objects.create(**self.hr_data)
        actual = HealthRecord.objects.get(pk=hr.id)
        self.assertEqual(hr.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(hr.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertLessEqual(0,
                             actual.temperature)
        self.assertLessEqual(0,
                             actual.respiratory_rate)
        self.assertLessEqual(0,
                             actual.heart_rate)
        self.assertLessEqual(0,
                             actual.blood_pressure)
        self.assertLessEqual(0,
                             actual.weight)
        self.assertLessEqual(0,
                             actual.body_condition_score)
        self.assertLessEqual(hr.status.name,
                             actual.status.name)

    def test_05_full_update(self):
        expected = HealthRecord.objects.get(id=1)
        expected.recorded_by = self.hr_data['recorded_by']
        expected.cow = self.hr_data['cow']
        expected.temperature = self.hr_data['temperature']
        expected.respiratory_rate = self.hr_data['respiratory_rate']
        expected.heart_rate = self.hr_data['heart_rate']
        expected.blood_pressure = self.hr_data['blood_pressure']
        expected.weight = self.hr_data['weight']
        expected.body_condition_score = self.hr_data['body_condition_score']
        expected.status = self.hr_data['status']
        expected.save()
        actual = HealthRecord.objects.get(id=expected.id)
        self.assertEqual(expected.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(expected.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertLessEqual(0,
                             actual.temperature)
        self.assertLessEqual(0,
                             actual.respiratory_rate)
        self.assertLessEqual(0,
                             actual.heart_rate)
        self.assertLessEqual(0,
                             actual.blood_pressure)
        self.assertLessEqual(0,
                             actual.weight)
        self.assertLessEqual(0,
                             actual.body_condition_score)
        self.assertLessEqual(expected.status.name,
                             actual.status.name)
                             
    def test_06_delete(self):
        expected = HealthRecord.objects.get(id=1)
        expected.delete()
        with self.assertRaises(HealthRecord.DoesNotExist) as context:
            HealthRecord.objects.get(pk=expected.id)
        msg = 'HealthRecord matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = HealthRecord()
        expected.recorded_by = self.hr_data['recorded_by']
        expected.cow = self.hr_data['cow']
        expected.temperature = self.hr_data['temperature']
        expected.respiratory_rate = self.hr_data['respiratory_rate']
        expected.heart_rate = self.hr_data['heart_rate']
        expected.blood_pressure = self.hr_data['blood_pressure']
        expected.weight = self.hr_data['weight']
        expected.body_condition_score = self.hr_data['body_condition_score']
        expected.status = self.hr_data['status']
        expected.save()
        actual = HealthRecord.objects.get(pk=expected.id)
        self.assertEqual(expected.recorded_by.username,
                         actual.recorded_by.username)
        self.assertEqual(expected.cow.breed.name,
                         actual.cow.breed.name)        
        self.assertLessEqual(0,
                             actual.temperature)
        self.assertLessEqual(0,
                             actual.respiratory_rate)
        self.assertLessEqual(0,
                             actual.heart_rate)
        self.assertLessEqual(0,
                             actual.blood_pressure)
        self.assertLessEqual(0,
                             actual.weight)
        self.assertLessEqual(0,
                             actual.body_condition_score)
        self.assertLessEqual(expected.status.name,
                             actual.status.name)
