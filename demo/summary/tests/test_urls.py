from rest_framework.reverse import django_reverse
from rest_framework.test import APITestCase

class TestSummaryAnnualAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_annual(self):
        expected = '/summary/api/annual/2018/'
        self.assertEqual(expected,
                         django_reverse('summary:annual',
                                        args=('2018',)))

class TestSummaryMonthlyAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_monthly(self):
        expected = '/summary/api/monthly/2018/03/'
        self.assertEqual(expected,
                         django_reverse('summary:monthly',
                                        args=('2018', '03')))
