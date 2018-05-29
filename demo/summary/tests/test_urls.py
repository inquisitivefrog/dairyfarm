from rest_framework.reverse import django_reverse
from rest_framework.test import APITestCase

class TestSummaryAnnualAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_annual_client(self):
        expected = '/summary/api/annual/client/1/'
        self.assertEqual(expected,
                         django_reverse('summary:annual-client',
                                        kwargs={'pk': 1}))

    def test_02_annual_client_year(self):
        expected = '/summary/api/annual/client/1/year/2015/'
        self.assertEqual(expected,
                         django_reverse('summary:annual-client-year',
                                        kwargs={'pk': 1,
                                                'year': 2015}))

class TestSummaryMonthlyAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_monthly_client_year(self):
        expected = '/summary/api/monthly/client/2/year/2018/'
        self.assertEqual(expected,
                         django_reverse('summary:monthly-client-year',
                                        kwargs={'pk': 2,
                                                'year': 2018}))

    def test_02_monthly_client_year_month(self):
        expected = '/summary/api/monthly/client/2/year/2018/month/3/'
        self.assertEqual(expected,
                         django_reverse('summary:monthly-client-year-month',
                                        kwargs={'pk': 2,
                                                'year': 2018,
                                                'month': 3}))
