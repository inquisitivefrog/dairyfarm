from random import randint

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from assets.models import Age, Breed, BreedImage, Color, Cow
from assets.serializers import CowSerializer, EventSerializer
from assets.serializers import ExerciseSerializer, HealthRecordSerializer
from assets.serializers import MilkSerializer, PastureSerializer
from assets.tests.utils import get_purchase_date, get_random_user

class TestCowSerializer(APITestCase):
    # note: order matters when loading fixtures
    fixtures = ['age', 'breed', 'breedimage', 'color', 'user', 'cow']

    def setUp(self):
        user = User.objects.get(username=get_random_user())
        ages = Age.objects.all()
        age = ages[randint(0, len(ages) - 1)]
        colors = Color.objects.all()
        color = colors[randint(0, len(colors) - 1)]
        images = BreedImage.objects.all()
        image = images[randint(0, len(images) - 1)]
        self.cow_data = {'purchased_by': user,
                         'purchase_date': get_purchase_date(),
                         'age': age,
                         'color': color,
                         'image': image}

    def tearDown(self):
        self.cow_data = None

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
        self.assertEqual(13,
                         len(colors))
        herd = Cow.objects.all()
        self.assertEqual(70,
                         len(herd))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))

    def test_01_create(self):
        actual = CowSerializer(data=self.cow_data)
        self.assertTrue(actual.is_valid())
        self.assertEqual(0,
                         len(actual.errors))
        print('DEBUG: data: {}'.format(self.cow_data))
        print('DEBUG: errors: {}'.format(actual.errors))
        actual.save()
        self.assertIn('purchased_by',
                      actual.data)
        self.assertIn('purchased_date',
                      actual.data)
        self.assertIn('age',
                      actual.data)
        self.assertIn('color',
                      actual.data)
        self.assertIn('image',
                      actual.data)

    def test_03_retrieve(self):
        cow = Cow.objects.get(id=1)
        actual = CowSerializer(cow)
        self.assertEqual(get_random_user(),
                         actual.data['purchased_by'])
        self.assertRegex(actual.data['purchase_date'],
                         '^\d{4}-\d{2}-\d{2}$')
        self.assertRegex(actual.data['age'],
                         '\d year')
        self.assertRegex(actual.data['color'],
                         '\w_\w')
        self.assertRegex(actual.data['image'].lower(),
                         '\w')
