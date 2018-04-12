from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from assets.models import Age, Breed, Color, Cow, HealthRecord, Illness
from assets.models import Injury, Milk, Status, Treatment, Vaccine

from summary.models import Annual, Monthly
from summary.serializers import AnnualReadSerializer, AnnualWriteSerializer
from summary.serializers import MonthlyReadSerializer, MonthlyWriteSerializer
from summary.tests.utils import TestData, TestTime

class TestAnnualReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'illness', 'injury', 'status',
                'treatment', 'user', 'vaccine', 'cow', 'healthrecord',
                'milk', 'annual']

    def setUp(self):
        self._load_model_data()

    def tearDown(self):
        self.model_data = None

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_username())
        self.model_data = {'created_by': user,
                           'year': TestTime.get_random_year()}

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

    def test_01_retrieve(self):
        annual = Annual.objects.get(id=1)
        actual = AnnualReadSerializer(annual)
        self.assertEqual(annual.created_by.username,
                         actual.data['created_by'])
        self.assertEqual(annual.year,
                         actual.data['year'])
        self.assertEqual(annual.total_cows,
                         actual.data['total_cows'])
        self.assertEqual(annual.aged_cows,
                         actual.data['aged_cows'])
        self.assertEqual(annual.pregnant_cows,
                         actual.data['pregnant_cows'])
        self.assertEqual(annual.ill_cows,
                         actual.data['ill_cows'])
        self.assertEqual(annual.injured_cows,
                         actual.data['injured_cows'])
        self.assertEqual(annual.gallons_milk,
                         actual.data['gallons_milk'])
        self.assertEqual(annual.link,
                         actual.data['link'])

    def test_02_list(self):
        expected = 10
        calendar = []
        for i in range(expected):
            self._load_model_data()
            annual = Annual.objects.create(**self.model_data)
            calendar.append(annual)
        actual = AnnualReadSerializer(calendar,
                                      many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('created_by',
                          actual.data[i])
            self.assertIn('year',
                          actual.data[i])
            self.assertIn('total_cows',
                          actual.data[i])
            self.assertIn('aged_cows',
                          actual.data[i])
            self.assertIn('pregnant_cows',
                          actual.data[i])
            self.assertIn('ill_cows',
                          actual.data[i])
            self.assertIn('injured_cows',
                          actual.data[i])
            self.assertIn('gallons_milk',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestAnnualWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'illness', 'injury', 'status',
                'treatment', 'user', 'vaccine', 'cow', 'healthrecord',
                'milk', 'annual']


    def setUp(self):
        self._load_annual_data()

    def tearDown(self):
        self.annual_data = None

    def _load_annual_data(self):
        user = User.objects.get(username=TestData.get_random_username())
        self.annual_data = {'created_by': user,
                            'year': TestTime.get_random_year()}

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

    def test_01_create(self):
        actual = AnnualWriteSerializer(data=self.annual_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertEqual(self.annual_data['created_by'].username,
                         actual.data['created_by'])
        self.assertEqual(self.annual_data['year'],
                         str(actual.data['year']))

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_annual_data()
            data.append(self.annual_data)
        actual = AnnualWriteSerializer(data=data,
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
            self.assertRegex(actual.data[i]['created_by'],
                             '\w')
            self.assertIsInstance(actual.data[i]['year'],
                                  int)

    def test_03_partial_update(self):
        annual = Annual.objects.get(id=1)
        self._load_annual_data()
        del self.annual_data['created_by']
        actual = AnnualWriteSerializer(annual,
                                       data=self.annual_data,
                                       partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('created_by',
                      actual.data)
        self.assertEqual(self.annual_data['year'],
                         str(actual.data['year']))

class TestMonthlyReadSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'illness', 'injury', 'status',
                'treatment', 'user', 'vaccine', 'cow', 'healthrecord',
                'milk', 'monthly']

    def setUp(self):
        self._load_model_data()

    def tearDown(self):
        self.model_data = None

    def _load_model_data(self):
        user = User.objects.get(username=TestData.get_random_username())
        self.model_data = {'created_by': user,
                           'year': TestTime.get_random_year(),
                           'month': TestTime.get_random_month()}

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

    def test_01_retrieve(self):
        expected = Monthly.objects.get(id=1)
        actual = MonthlyReadSerializer(expected)
        self.assertEqual(expected.created_by.username,
                         actual.data['created_by'])
        self.assertEqual(expected.year,
                         actual.data['year'])
        self.assertEqual(expected.month,
                         actual.data['month'])
        self.assertEqual(expected.total_cows,
                         actual.data['total_cows'])
        self.assertEqual(expected.aged_cows,
                         actual.data['aged_cows'])
        self.assertEqual(expected.pregnant_cows,
                         actual.data['pregnant_cows'])
        self.assertEqual(expected.ill_cows,
                         actual.data['ill_cows'])
        self.assertEqual(expected.injured_cows,
                         actual.data['injured_cows'])
        self.assertEqual(expected.gallons_milk,
                         actual.data['gallons_milk'])
        self.assertEqual(expected.link,
                         actual.data['link'])

    def test_02_list(self):
        expected = 10
        calendar = []
        for i in range(expected):
            self._load_model_data()
            month = Monthly.objects.create(**self.model_data)
            calendar.append(month)
        actual = MonthlyReadSerializer(calendar,
                                       many=True)
        self.assertEqual(expected,
                         len(actual.data))
        for i in range(expected):
            self.assertIn('id',
                          actual.data[i])
            self.assertIn('created_by',
                          actual.data[i])
            self.assertIn('year',
                          actual.data[i])
            self.assertIn('month',
                          actual.data[i])
            self.assertIn('total_cows',
                          actual.data[i])
            self.assertIn('aged_cows',
                          actual.data[i])
            self.assertIn('pregnant_cows',
                          actual.data[i])
            self.assertIn('ill_cows',
                          actual.data[i])
            self.assertIn('injured_cows',
                          actual.data[i])
            self.assertIn('gallons_milk',
                          actual.data[i])
            self.assertIn('link',
                          actual.data[i])

class TestMonthlyWriteSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'color', 'illness', 'injury', 'status',
                'treatment', 'user', 'vaccine', 'cow', 'healthrecord',
                'milk', 'monthly']

    def setUp(self):
        self._load_monthly_data()

    def tearDown(self):
        self.monthly_data = None

    def _load_monthly_data(self):
        user = User.objects.get(username=TestData.get_random_username())
        self.monthly_data = {'created_by': user,
                             'year': TestTime.get_random_year(),
                             'month': TestTime.get_random_month()}

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

    def test_01_create(self):
        actual = MonthlyWriteSerializer(data=self.monthly_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertEqual(self.monthly_data['created_by'].username,
                         actual.data['created_by'])
        self.assertEqual(self.monthly_data['year'],
                         str(actual.data['year']))
        self.assertEqual(int(self.monthly_data['month']),
                         actual.data['month'])

    def test_02_bulk_create(self):
        expected = 10
        data = []
        for i in range(expected):
            self._load_monthly_data()
            data.append(self.monthly_data)
        actual = MonthlyWriteSerializer(data=data,
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
            self.assertRegex(actual.data[i]['created_by'],
                             '\w')
            self.assertIsInstance(actual.data[i]['year'],
                                  int)
            self.assertIsInstance(actual.data[i]['month'],
                                  int)

    def test_03_partial_update(self):
        month = Monthly.objects.get(id=1)
        self._load_monthly_data()
        del self.monthly_data['created_by']
        actual = MonthlyWriteSerializer(month,
                                        data=self.monthly_data,
                                        partial=True)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        actual.save()
        self.assertIn('id',
                      actual.data)
        self.assertIn('created_by',
                      actual.data)
        self.assertEqual(self.monthly_data['year'],
                         str(actual.data['year']))
        self.assertEqual(int(self.monthly_data['month']),
                         actual.data['month'])

