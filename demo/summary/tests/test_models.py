from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from assets.models import Age, Breed, Client, Color, Cow, HealthRecord, Illness
from assets.models import Injury, Milk, Status, Treatment, Vaccine

from summary.models import Annual, Monthly
from summary.tests.utils import TestData, TestTime

class TestAnnualModel(APITestCase):
    fixtures = ['age', 'breed', 'user', 'color', 'illness', 'injury',
                'status', 'treatment', 'client', 'vaccine', 'cow',
                'healthrecord', 'milk', 'monthly', 'annual']


    def setUp(self):
        client = Client.objects.get(name=TestData.get_random_client())
        user = User.objects.get(username=TestData.get_random_username())
        self.annual_data = {'client': client, 
                            'created_by': user,
                            'year': 2015}
        self.pk = 1

    def tearDown(self):
        self.annual_data = None

    def test_00_load_fixtures(self):
        annual = Annual.objects.all()
        self.assertLessEqual(1,
                             len(annual))
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        hr = HealthRecord.objects.all()
        self.assertLessEqual(10,
                             len(hr))
        milk = Milk.objects.all()
        self.assertLessEqual(10,
                             len(milk))

    def test_01_object(self):
        a = Annual()
        self.assertEqual("<class 'summary.models.Annual'>",
                         repr(a))
        self.assertEqual("<class 'summary.models.Annual'>",
                         str(a))
        a = Annual.objects.get(pk=1)
        self.assertEqual("<class 'summary.models.Annual'>:{}".format(a.id),
                         repr(a))
        self.assertEqual(str(a.id),
                         str(a))
 
    def test_02_get(self):
        a = Annual.objects.get(id=self.pk)
        self.assertRegex(a.created_by.username,
                         '\w')
        self.assertLessEqual(2015,
                             a.year)
        self.assertLessEqual(1,
                             a.total_cows)
        self.assertLessEqual(0,
                             a.aged_cows)
        self.assertLessEqual(0,
                             a.pregnant_cows)
        self.assertLessEqual(0,
                             a.ill_cows)
        self.assertLessEqual(0,
                             a.injured_cows)
        self.assertLessEqual(1,
                             a.gallons_milk)

    def test_03_filter(self):
        expected = Annual.objects.filter(year='2015')
        actual = Annual.objects.filter(year__endswith='15')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        a = Annual.objects.create(**self.annual_data)
        self.assertEqual(self.annual_data['created_by'],
                         a.created_by)
        self.assertEqual(self.annual_data['year'],
                         a.year)

    def test_05_partial_update(self):
        expected = Annual.objects.get(id=self.pk)
        user = User.objects.get(username='vet')
        expected.created_by = user
        expected.save()
        actual = Annual.objects.get(id=expected.id)
        self.assertEqual(expected.created_by.username,
                         actual.created_by.username)
                             
    def test_06_delete(self):
        expected = Annual.objects.get(id=self.pk)
        expected.delete()
        with self.assertRaises(Annual.DoesNotExist) as context:
            Annual.objects.get(pk=expected.id)
        msg = 'Annual matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        year = 2025
        expected = Annual()
        expected.client = self.annual_data['client']
        expected.created_by = self.annual_data['created_by']
        expected.year = year
        expected.save()
        actual = Annual.objects.get(pk=expected.id)
        self.assertEqual(expected.created_by,
                         actual.created_by)
        self.assertEqual(expected.year,
                         year)
        self.assertLessEqual(0,
                             actual.total_cows)
        self.assertLessEqual(0,
                             actual.aged_cows)
        self.assertLessEqual(0,
                             actual.pregnant_cows)
        self.assertLessEqual(0,
                             actual.ill_cows)
        self.assertLessEqual(0,
                             actual.injured_cows)
        self.assertLessEqual(0,
                             actual.gallons_milk)

class TestMonthlyModel(APITestCase):
    fixtures = ['age', 'breed', 'user', 'color', 'illness', 'injury',
                'status', 'treatment', 'client', 'vaccine', 'cow',
                'healthrecord', 'milk', 'monthly']

    def setUp(self):
        client = Client.objects.get(name=TestData.get_random_client())
        user = User.objects.get(username=TestData.get_random_username())
        self.pk = 1
        self.monthly_data = {'client': client,
                             'created_by': user,
                             'year': 2017,
                             'month': 1}

    def tearDown(self):
        self.monthly_data = None

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertLessEqual(10,
                             len(herd))
        hr = HealthRecord.objects.all()
        self.assertLessEqual(10,
                             len(hr))
        milk = Milk.objects.all()
        self.assertLessEqual(10,
                             len(milk))
        months = Monthly.objects.all()
        self.assertLessEqual(1,
                             len(months))

    def test_01_object(self):
        m = Monthly()
        self.assertEqual("<class 'summary.models.Monthly'>",
                         repr(m))
        self.assertEqual("<class 'summary.models.Monthly'>",
                         str(m))
        m = Monthly.objects.get(pk=1)
        self.assertEqual("<class 'summary.models.Monthly'>:{}".format(m.id),
                         repr(m))
        self.assertEqual(str(m.id),
                         str(m))
 
    def test_02_get(self):
        m = Monthly.objects.get(id=self.pk)
        self.assertRegex(m.created_by.username,
                         '\w')
        self.assertLessEqual(2014,
                             m.year)
        self.assertLessEqual(1,
                             m.month)
        self.assertLessEqual(1,
                             m.total_cows)
        self.assertLessEqual(0,
                             m.aged_cows)
        self.assertLessEqual(0,
                             m.pregnant_cows)
        self.assertLessEqual(0,
                             m.ill_cows)
        self.assertLessEqual(0,
                             m.injured_cows)
        self.assertLessEqual(1,
                             m.gallons_milk)

    def test_03_filter(self):
        expected = Monthly.objects.filter(year='2015',
                                          month='10')
        actual = Monthly.objects.filter(year__endswith='15',
                                        month__endswith='0')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        m = Monthly.objects.create(**self.monthly_data)
        self.assertEqual(self.monthly_data['created_by'],
                         m.created_by)
        self.assertEqual(self.monthly_data['year'],
                         m.year)
        self.assertEqual(self.monthly_data['month'],
                         m.month)

    def test_05_partial_update(self):
        expected = Monthly.objects.get(id=self.pk)
        user = User.objects.get(username='vet')
        expected.created_by = user
        expected.save()
        actual = Monthly.objects.get(id=expected.id)
        self.assertEqual(expected.created_by.username,
                         actual.created_by.username)
        self.assertEqual(expected.year,
                         actual.year)
        self.assertEqual(expected.month,
                         actual.month)
                             
    def test_06_delete(self):
        expected = Monthly.objects.get(id=self.pk)
        expected.delete()
        with self.assertRaises(Monthly.DoesNotExist) as context:
            Monthly.objects.get(pk=expected.id)
        msg = 'Monthly matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_07_save(self):
        expected = Monthly()
        expected.created_by = self.monthly_data['created_by']
        expected.year = self.monthly_data['year']
        expected.month = self.monthly_data['month']
        expected.save()
        actual = Monthly.objects.get(pk=expected.id)
        self.assertEqual(expected.created_by,
                         actual.created_by)
        self.assertEqual(expected.year,
                         actual.year)
        self.assertEqual(int(expected.month),
                         actual.month)
        self.assertLessEqual(0,
                             actual.total_cows)
        self.assertLessEqual(0,
                             actual.aged_cows)
        self.assertLessEqual(0,
                             actual.pregnant_cows)
        self.assertLessEqual(0,
                             actual.ill_cows)
        self.assertLessEqual(0,
                             actual.injured_cows)
        self.assertLessEqual(0,
                             actual.gallons_milk)
