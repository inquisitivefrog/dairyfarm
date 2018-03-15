from random import randint
from uuid import uuid4

from django.utils.timezone import datetime, localtime, pytz

class TestData:
    @classmethod
    def get_action(cls):
        return 'Burp'

    @classmethod
    def get_breed(cls):
        return 'Criollo'

    @classmethod
    def get_cereal(cls):
        return 'maize'

    @classmethod
    def get_grass(cls):
        return 'quackgrass'

    @classmethod
    def get_illness(cls):
        return 'mad cow'

    @classmethod
    def get_injury(cls):
        return 'tipped over'

    @classmethod
    def get_legume(cls):
        return 'sainfoin'

    @classmethod
    def get_pasture(cls):
        return 'Hill'

    @classmethod
    def get_region(cls):
        return 'Dead Center'

    @classmethod
    def get_regionimage(cls):
        return '/static/images/breeds/belgian_blue.png'

    @classmethod
    def get_rfid(cls):
        return uuid4()

    @classmethod
    def get_season(cls):
        return 'Fall'

    @classmethod
    def get_status(cls):
        return 'Retired'

    @classmethod
    def get_treatment(cls):
        return 'apply heating pad'

    @classmethod
    def get_vaccine(cls):
        return 'cow pox vaccine'

    @classmethod
    def get_distance(cls):
        distance = randint(1, 3)
        return distance

    @classmethod
    def get_random_age(cls):
        age = randint(6, 10)
        return '{} years'.format(age)

    @classmethod
    def get_random_breed(cls):
        breeds = ['Criollo', 'Pineywood', 'Randall', 'Belgian Blue',
                  'American Milking Devon', 'Guzerat', 'Red Sindhi']
        breed = randint(0, len(breeds) - 1)
        return breeds[breed]

    @classmethod
    def get_random_color(cls):
        colors = ['Blue', 'Green', 'Orange', 'Yellow']
        color = randint(0, len(colors) - 1)
        return colors[color]

    @classmethod
    def get_random_image(cls):
        images = ['/static/images/criollo.png',
                  '/static/images/pineywood.png',
                  '/static/images/randall.png',
                  '/static/images/belgian_blue.png',
                  '/static/images/american_milking_devon.png',
                  '/static/images/guzerat.png',
                  '/static/images/red_sindhi.png']
        image = randint(0, len(images) - 1)
        return images[image]

    @classmethod
    def get_random_user(cls):
        return 'farmhand'

    @classmethod
    def get_temp(cls):
        # ideal healthy temp range: 100.4 - 102.0
        return randint(1004, 1020) * 10.0 / 100

    @classmethod
    def get_resp(cls):
        # ideal healthy resp range: 26 - 50
        return randint(260, 500) * 10.0 / 100

    @classmethod
    def get_hr(cls):
        # ideal healthy HR range: 48 - 84
        return randint(480, 840) * 10.0 / 100

    @classmethod
    def get_bp(cls):
        # ideal healthy BP range: 130 - 150
        return randint(1300, 1500) * 10.0 / 100

    @classmethod
    def get_bcs(cls):
        # ideal healthy BCS range: 3.0 - 3.5
        return randint(30, 35) * 10.0 / 100

    @classmethod
    def get_weight(cls):
        # ideal healthy weight range: 450 - 550
        return randint(450, 550)

class TestTime:
    @classmethod
    def get_purchase_date(cls):
        return '2014-12-31'

    @classmethod
    def convert_date(cls, t):
        return datetime.strftime(t, '%Y-%m-%d')

    @classmethod
    def get_date(cls):
        t = datetime.now()
        return datetime.date(t)

    @classmethod
    def get_datetime(cls):
        t = datetime.now()
        if t.month < 10:
            month = '0{}'.format(t.month)
        else:
            month = '{}'.format(t.month)
        if t.day < 10:
            day = '0{}'.format(t.day)
        else:
            day = '{}'.format(t.day)
        if t.hour < 10:
            hour = '0{}'.format(t.hour)
        else:
            hour = '{}'.format(t.hour)
        if t.minute < 10:
            minute = '0{}'.format(t.minute)
        else:
            minute = '{}'.format(t.minute)
        if t.second < 10:
            second = '0{}'.format(t.second)
        else:
            second = '{}'.format(t.second)
        return ('{}-{}-{} {}:{}:{}.{}+00:00'.format(t.year,
                                                    month,
                                                    day,
                                                    hour,
                                                    minute,
                                                    second,
                                                    t.microsecond))

