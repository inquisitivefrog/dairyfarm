from random import randint

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from assets.models import Age, Breed, Color, Cow, Image
from assets.tests.utils import get_random_age, get_random_breed
from assets.tests.utils import get_random_color, get_random_image
from assets.tests.utils import get_random_user, convert_date, get_today

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
        self.assertEqual('Age object (None)',
                         str(a))
 
    def test_02_get(self):
        a = Age.objects.get(id=1)
        self.assertEqual('1 year',
                         a.name)        

    def test_03_filter(self):
        expected = Age.objects.filter(name='1 year')
        actual = Age.objects.filter(name__endswith='r')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        a = Age.objects.create(**self.age_data)
        self.assertEqual(self.age_data['name'],
                         a.name)

    def test_05_full_update(self):
        expected = Age.objects.get(id=1)
        expected.name = get_random_age()
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
        self.breed_data = {'name': 'Criollo'}

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
        self.assertEqual('Breed object (None)',
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

    def test_05_full_update(self):
        expected = Breed.objects.get(id=1)
        expected.name = get_random_breed()
        expected.save()
        actual = Breed.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
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
        expected.save()
        actual = Breed.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestColorModel(APITestCase):
    fixtures = ['breed', 'color']

    def setUp(self):
        self.breed_data = {'name': 'Belgian Blue'}
        self.color_data = {'name': 'blue'}

    def tearDown(self):
        self.breed_data = None
        self.color_data = None

    def test_00_load_fixtures(self):
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        colors = Color.objects.all()
        self.assertEqual(13,
                         len(colors))

    def test_01_object(self):
        c = Color()
        self.assertEqual("<class 'assets.models.Color'>",
                         repr(c))
        self.assertEqual('Color object (None)',
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
        b = Breed.objects.create(**self.breed_data)
        self.color_data.update({'breed': b})
        c = Color.objects.create(**self.color_data)
        self.assertEqual(self.color_data['name'],
                         c.name)

    def test_05_full_update(self):
        expected = Color.objects.get(id=1)
        expected.name = get_random_color()
        breeds = Breed.objects.filter(id__gt=1) 
        expected.breed = breeds[randint(1, len(breeds) - 1)]
        expected.save()
        actual = Color.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
        self.assertEqual(expected.breed,
                         actual.breed)
                             
    def test_06_partial_update(self):
        expected = Color.objects.get(id=1)
        expected.name = get_random_color()
        expected.save()
        actual = Color.objects.get(id=expected.id)
        self.assertEqual(expected.name,
                         actual.name)
                             
    def test_07_delete(self):
        expected = Color.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Color.DoesNotExist) as context:
            Color.objects.get(pk=expected.id)
        msg = 'Color matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_08_save(self):
        expected = Color()
        expected.name = self.color_data['name']
        expected.save()
        actual = Color.objects.get(pk=expected.id)
        self.assertEqual(expected.name,
                         actual.name)

class TestImageModel(APITestCase):
    fixtures = ['breed', 'image']

    def setUp(self):
        self.breed_data = {'name': 'Belgian Blue'}
        self.image_data = {'url': '/static/images/belgian_blue.png'}

    def tearDown(self):
        self.breed_data = None
        self.image_data = None

    def test_00_load_fixtures(self):
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        images = Image.objects.all()
        self.assertEqual(7,
                         len(images))

    def test_01_object(self):
        i = Image()
        self.assertEqual("<class 'assets.models.Image'>",
                         repr(i))
        self.assertEqual('Image object (None)',
                         str(i))
 
    def test_02_get(self):
        i = Image.objects.get(id=1)
        self.assertEqual('/static/images/holstein.png',
                         i.url)        

    def test_03_filter(self):
        expected = Image.objects.filter(url='/static/images/holstein.png')
        actual = Image.objects.filter(url__endswith='stein.png')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        b = Breed.objects.create(**self.breed_data)
        self.image_data.update({'breed': b})
        i = Image.objects.create(**self.image_data)
        self.assertEqual(self.image_data['url'],
                         i.url)

    def test_05_full_update(self):
        expected = Image.objects.get(id=1)
        expected.url = get_random_image()
        breeds = Breed.objects.filter(id__gt=1) 
        expected.breed = breeds[randint(1, len(breeds) - 1)]
        expected.save()
        actual = Image.objects.get(id=expected.id)
        self.assertEqual(expected.url,
                         actual.url)
        self.assertEqual(expected.breed,
                         actual.breed)
                             
    def test_06_partial_update(self):
        expected = Image.objects.get(id=1)
        expected.url = get_random_image()
        expected.save()
        actual = Image.objects.get(id=expected.id)
        self.assertEqual(expected.url,
                         actual.url)

    def test_07_delete(self):
        expected = Image.objects.get(id=1)
        expected.delete()
        with self.assertRaises(Image.DoesNotExist) as context:
            Image.objects.get(pk=expected.id)
        msg = 'Image matching query does not exist'
        self.assertIn(msg, str(context.exception))

    def test_08_save(self):
        b = Breed.objects.create(**self.breed_data)
        expected = Image()
        expected.url = self.image_data['url']
        expected.breed = b
        expected.save()
        actual = Image.objects.get(pk=expected.id)
        self.assertEqual(expected.url,
                         actual.url)

class TestCowModel(APITestCase):
    fixtures = ['age', 'breed', 'color', 'cow', 'image', 'user']

    def setUp(self):
        self.age_data = {'name': '10 years'}
        self.breed_data = {'name': 'Belgian Blue'}
        self.color_data = {'name': 'blue'}
        self.cow_data = {'purchased_by': User.objects.get(username=get_random_user()),
                         'purchase_date': get_today()}
        self.image_data = {'url': '/static/images/belgian_blue.png'}

    def tearDown(self):
        self.age_data = None
        self.breed_data = None
        self.color_data = None
        self.image_data = None

    def test_00_load_fixtures(self):
        ages = Age.objects.all()
        self.assertEqual(5,
                         len(ages))
        breeds = Breed.objects.all()
        self.assertEqual(7,
                         len(breeds))
        colors = Color.objects.all()
        self.assertEqual(13,
                         len(colors))
        cows = Cow.objects.all()
        self.assertEqual(70,
                         len(cows))
        images = Image.objects.all()
        self.assertEqual(7,
                         len(images))
        users = User.objects.all()
        self.assertEqual(3,
                         len(users))

    def test_01_object(self):
        c = Cow()
        self.assertEqual("<class 'assets.models.Cow'>",
                         repr(c))
        self.assertEqual('Cow object (None)',
                         str(c))
 
    def test_02_get(self):
        c = Cow.objects.get(id=1)
        self.assertEqual('1 year',
                         c.age.name)
        self.assertEqual('Holstein',
                         c.breed.name)
        self.assertEqual('black_white',
                         c.color.name)
        self.assertEqual('/static/images/holstein.png',
                         c.image.url)
        self.assertEqual('2018-01-26',
                         convert_date(c.purchase_date))
        self.assertEqual(get_random_user(),
                         c.purchased_by.username)

    def test_03_filter(self):
        expected = Cow.objects.filter(image__url='/static/images/holstein.png')
        actual = Cow.objects.filter(image__url__endswith='stein.png')
        self.assertEqual(len(expected),
                         len(actual))

    def test_04_create(self):
        a = Age.objects.create(**self.age_data)
        b = Breed.objects.create(**self.breed_data)
        self.color_data.update({'breed': b})
        c = Color.objects.create(**self.color_data)
        self.image_data.update({'breed': b})
        i = Image.objects.create(**self.image_data)
        self.cow_data.update({'age': a,
                              'breed': b,
                              'color': c,
                              'image': i})
        actual = Cow.objects.create(**self.cow_data)
        self.assertEqual(self.age_data['name'],
                         actual.age.name)
        self.assertEqual(self.breed_data['name'],
                         actual.breed.name)
        self.assertEqual(self.color_data['name'],
                         actual.color.name)
        self.assertEqual(self.image_data['url'],
                         actual.image.url)
        self.assertEqual(self.cow_data['purchase_date'],
                         actual.purchase_date)
        self.assertEqual(self.cow_data['purchased_by'],
                         actual.purchased_by)

    def test_05_full_update(self):
        a = Age.objects.create(**self.age_data)
        b = Breed.objects.create(**self.breed_data)
        self.color_data.update({'breed': b})
        c = Color.objects.create(**self.color_data)
        self.image_data.update({'breed': b})
        i = Image.objects.create(**self.image_data)
        u = User.objects.get(username=get_random_user())
        d = get_today()
        expected = Cow.objects.get(id=1)
        expected.age = a
        expected.breed = b
        expected.color = c
        expected.image = i
        expected.purchased_by = u
        expected.purchase_date = d
        expected.save()
        actual = Cow.objects.get(id=expected.id)
        self.assertEqual(expected.age.name,
                         actual.age.name)
        self.assertEqual(expected.breed.name,
                         actual.breed.name)
        self.assertEqual(expected.color.name,
                         actual.color.name)
        self.assertEqual(expected.image.url,
                         actual.image.url)
                             
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
        self.color_data.update({'breed': b})
        c = Color.objects.create(**self.color_data)
        self.image_data.update({'breed': b})
        i = Image.objects.create(**self.image_data)
        u = User.objects.get(username=get_random_user())
        expected = Cow()
        expected.age = a
        expected.breed = b
        expected.color = c
        expected.image = i
        expected.purchased_by = u
        expected.save()
        actual = Cow.objects.get(pk=expected.id)
        self.assertEqual(expected.age.name,
                         actual.age.name)
        self.assertEqual(expected.breed.name,
                         actual.breed.name)
        self.assertEqual(expected.color.name,
                         actual.color.name)
        self.assertEqual(expected.image.url,
                         actual.image.url)
