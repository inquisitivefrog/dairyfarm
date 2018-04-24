from rest_framework.reverse import django_reverse
from rest_framework.test import APITestCase

class TestAssetsURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_index(self):
        expected = '/assets/'
        self.assertEqual(expected,
                         django_reverse('assets:index'))

class TestAssetsCowAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_cow_list(self):
        expected = '/assets/api/cows/'
        self.assertEqual(expected,
                         django_reverse('assets:cow-list'))

    def test_02_cow_list_month(self):
        expected = '/assets/api/cows/year/2018/month/03/'
        self.assertEqual(expected,
                         django_reverse('assets:cow-list-month',
                                        args=('2018', '03')))

    def test_03_cow_list_year(self):
        expected = '/assets/api/cows/year/2018/'
        self.assertEqual(expected,
                         django_reverse('assets:cow-list-year',
                                        args=('2018',)))

    def test_04_cow_detail(self):
        expected = '/assets/api/cows/1/'
        self.assertEqual(expected,
                         django_reverse('assets:cow-detail',
                                        args=(1,)))

class TestAssetsEventAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_event_list(self):
        expected = '/assets/api/events/'
        self.assertEqual(expected,
                         django_reverse('assets:event-list'))

    def test_02_event_detail(self):
        expected = '/assets/api/events/1/'
        self.assertEqual(expected,
                         django_reverse('assets:event-detail',
                                        args=(1,)))

class TestAssetsExerciseAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_exercise_list(self):
        expected = '/assets/api/exercises/'
        self.assertEqual(expected,
                         django_reverse('assets:exercise-list'))

    def test_02_exercise_detail(self):
        expected = '/assets/api/exercises/1/'
        self.assertEqual(expected,
                         django_reverse('assets:exercise-detail',
                                        args=(1,)))

class TestAssetsHealthRecordAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_healthrecord_list(self):
        expected = '/assets/api/healthrecords/'
        self.assertEqual(expected,
                         django_reverse('assets:healthrecord-list'))

    def test_02_healthrecord_detail(self):
        expected = '/assets/api/healthrecords/1/'
        self.assertEqual(expected,
                         django_reverse('assets:healthrecord-detail',
                                        args=(1,)))

class TestAssetsMilkAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_milk_list(self):
        expected = '/assets/api/milk/'
        self.assertEqual(expected,
                         django_reverse('assets:milk-list'))

    def test_02_milk_detail(self):
        expected = '/assets/api/milk/1/'
        self.assertEqual(expected,
                         django_reverse('assets:milk-detail',
                                        args=(1,)))

class TestAssetsSeedAPIURLConf(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_seed_list(self):
        expected = '/assets/api/seeds/'
        self.assertEqual(expected,
                         django_reverse('assets:seed-list'))

    def test_02_seed_detail(self):
        expected = '/assets/api/seeds/1/'
        self.assertEqual(expected,
                         django_reverse('assets:seed-detail',
                                        args=(1,)))
