from json import dumps
from random import randint

from django.contrib.auth.models import User
from django.utils.six import BytesIO

from rest_framework.parsers import JSONParser
from rest_framework.reverse import django_reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate

from assets.models import Client, Cow, HealthRecord, Milk

from summary.models import Annual, Monthly
from summary.api_views import AnnualSummaryByClientView, MonthlySummaryByClientView
from summary.tests.utils import TestData, TestTime

class TestAnnualSummaryByClientView(APITestCase):
    fixtures = ['age', 'breed', 'user', 'color', 'illness', 'injury',
                'status', 'treatment', 'client', 'vaccine', 'cow',
                'healthrecord', 'milk', 'annual']

    def setUp(self):
        self.client = Client.objects.get(name=TestData.get_random_client())
        self.user = User.objects.get(username=TestData.get_random_username())
        self.data = {'client': self.client.name,
                     'created_by': self.user.username,
                     'year': TestTime.get_random_year()}
        self.pk = 1
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.url = django_reverse('summary:annual-client-year',
                                  kwargs={'pk': self.pk,
                                          'year': self.data['year']})

    def tearDown(self):
        self.data = None
        self.factory = None
        self.user = None

    def test_00_load_fixtures(self):
        years = Annual.objects.all()
        self.assertLessEqual(1,
                             len(years))
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))
        hr = HealthRecord.objects.all()
        self.assertLessEqual(1,
                             len(hr))
        milk = Milk.objects.all()
        self.assertLessEqual(1,
                             len(milk))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = AnnualSummaryByClientView.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
        # unnecessary by design
        pass

    def test_03_retrieve(self):
        # by design, returns the most recent created
        annual = Annual.objects.get(pk=1)
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        kwargs = {'year': str(annual.year),
                  'pk': self.pk}
        response = AnnualSummaryByClientView.as_view()(request=request,
                                                       **kwargs)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_annual_read_keys():
            self.assertIn(key,
                          data[0])

    def test_04_create(self):
        request = self.factory.post(path=self.url,
                                    data=dumps(self.data),
                                    content_type=TestData.get_format(),
                                    follow=False)
        force_authenticate(request,
                           user=self.user)
        request.POST = self.data
        self.assertTrue(self.user.is_authenticated)
        response = AnnualSummaryByClientView.as_view()(request=request)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_annual_write_keys():
            self.assertIn(key,
                          data)

    def test_05_destroy(self):
        # unnecessary by design as assumed always needed for Sarbane Oxley
        pass

    def test_06_full_update(self):
        # unnecessary by design in favor of creating a replacement with newer data
        pass

    def test_07_partial_update(self):
        # unnecessary by design in favor of creating a replacement with newer data
        pass

class TestMonthlySummaryByClientView(APITestCase):
    fixtures = ['age', 'breed', 'user', 'color', 'illness', 'injury',
                'status', 'treatment', 'client', 'vaccine', 'cow',
                'healthrecord', 'milk', 'monthly']

    def setUp(self):
        self.user = User.objects.get(username=TestData.get_random_username())
        self.data = {'created_by': self.user.username,
                     'year': TestTime.get_random_year(),
                     'month': TestTime.get_random_month()}
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.url = django_reverse('summary:monthly-client-year-month',
                                  kwargs={'pk': 1,
                                          'year': self.data['year'],
                                          'month': self.data['month']})

    def tearDown(self):
        self.data = None
        self.factory = None
        self.user = None

    def test_00_load_fixtures(self):
        herd = Cow.objects.all()
        self.assertLessEqual(1,
                             len(herd))
        users = User.objects.all()
        self.assertLessEqual(1,
                             len(users))
        hr = HealthRecord.objects.all()
        self.assertLessEqual(1,
                             len(hr))
        milk = Milk.objects.all()
        self.assertLessEqual(1,
                             len(milk))
        months = Monthly.objects.all()
        self.assertLessEqual(1,
                             len(months))

    def test_01_options(self):
        request = self.factory.options(path=self.url,
                                       content_type=TestData.get_format())
        force_authenticate(request, user=self.user)
        self.assertTrue(self.user.is_authenticated)
        response = MonthlySummaryByClientView.as_view()(request=request)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        self.assertEquals(TestData.get_allowed_methods(),
                          response.get('allow'))
        self.assertEquals(TestData.get_content_type(),
                          response.get('content-type'))

    def test_02_list(self):
        # unnecessary by design
        pass

    def test_03_retrieve(self):
        # by design, returns the most recent created
        instance = Monthly.objects.get(pk=1)
        request = self.factory.get(path=self.url,
                                   content_type=TestData.get_format())
        force_authenticate(request,
                           user=self.user)
        self.assertTrue(self.user.is_authenticated)
        kwargs = {'pk': 1,
                  'year': str(instance.year),
                  'month': str(instance.month)}
        response = MonthlySummaryByClientView.as_view()(request=request,
                                                        **kwargs)
        self.assertEqual(200,
                         response.status_code)
        self.assertEqual('OK',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_monthly_read_keys():
            self.assertIn(key,
                          data[0])

    def test_04_create(self):
        self.data.update({'month': int(self.data['month'])})
        request = self.factory.post(path=self.url,
                                    data=dumps(self.data),
                                    content_type=TestData.get_format(),
                                    follow=False)
        force_authenticate(request,
                           user=self.user)
        request.POST = self.data
        self.assertTrue(self.user.is_authenticated)
        response = MonthlySummaryByClientView.as_view()(request=request)
        self.assertEqual(201,
                         response.status_code)
        self.assertEqual('Created',
                         response.reason_phrase)
        if not response.is_rendered:
             response = response.render()
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        for key in TestData.get_monthly_write_keys():
            self.assertIn(key,
                          data)

    def test_05_destroy(self):
        # unnecessary by design as assumed always needed for Sarbane Oxley
        pass

    def test_06_full_update(self):
        # unnecessary by design in favor of creating a replacement with newer data
        pass

    def test_07_partial_update(self):
        # unnecessary by design in favor of creating a replacement with newer data
        pass

