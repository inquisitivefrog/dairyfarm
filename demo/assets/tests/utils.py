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
    def get_pastureimage(cls):
        return '/static/images/regions/hill.jpg'

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
        return 'Autumn'

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
    def get_milk(cls):
        gallons = randint(3, 6)
        return gallons 

    @classmethod
    def get_age(cls):
        return '3 years'

    @classmethod
    def get_breed(cls):
        return 'Criollo'

    @classmethod
    def get_color(cls):
        return 'roan'

    @classmethod
    def get_image(cls):
        return '/static/images/breeds/criollo.png'
  
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
    def get_random_client(cls):
        clients = ['ACME Dairy Farm', 'Kraft Foods Cheese',
                   'Land O Lakes', 'Nestle USA', 'Dean Foods', 
                   'Saputo', 'Schreiber Foods']
        client = randint(0, len(clients) - 1)
        return clients[client]

    @classmethod
    def get_random_color(cls):
        colors = ['Blue', 'Green', 'Orange', 'Yellow']
        color = randint(0, len(colors) - 1)
        return colors[color]

    @classmethod
    def get_random_image(cls):
        images = ['/static/images/breeds/criollo.png',
                  '/static/images/breeds/pineywood.png',
                  '/static/images/breeds/randall.png',
                  '/static/images/breeds/belgian_blue.png',
                  '/static/images/breeds/american_milking_devon.png',
                  '/static/images/breeds/guzerat.png',
                  '/static/images/breeds/red_sindhi.png']
        image = randint(0, len(images) - 1)
        return images[image]

    @classmethod
    def get_random_user(cls):
        return 'foster'

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

    @classmethod
    def get_allowed_methods(cls):
        return 'GET, HEAD, OPTIONS'

    @classmethod
    def get_allowed_detail_methods(cls):
        return 'GET, PUT, PATCH, HEAD, OPTIONS'

    @classmethod
    def get_all_allowed_detail_methods(cls):
        return 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS'

    @classmethod
    def get_allowed_list_methods(cls):
        return 'GET, POST, HEAD, OPTIONS'

    @classmethod
    def get_content_length(cls):
        return '0'

    @classmethod
    def get_content_type(cls):
        return 'text/html; charset=utf-8'

    @classmethod
    def get_format(cls):
        return 'application/json'

    @classmethod
    def get_cow_read_keys(cls):
        return ['rfid', 'purchased_by', 'purchase_date', 'age', 'breed',
                'color', 'link']

    @classmethod
    def get_cow_write_keys(cls):
        return ['rfid', 'purchased_by', 'purchase_date', 'age', 'breed',
                'color']

    @classmethod
    def get_event_read_keys(cls):
        return ['id', 'recorded_by', 'cow', 'event_time', 'action', 'link']

    @classmethod
    def get_event_write_keys(cls):
        return ['id', 'recorded_by', 'cow', 'event_time', 'action']

    @classmethod
    def get_exercise_read_keys(cls):
        return ['id', 'recorded_by', 'pasture', 'exercise_time', 'link']

    @classmethod
    def get_exercise_write_keys(cls):
        return ['id', 'recorded_by', 'pasture', 'exercise_time']

    @classmethod
    def get_milk_read_keys(cls):
        return ['id', 'recorded_by', 'cow', 'milking_time', 'gallons', 'link']

    @classmethod
    def get_milk_write_keys(cls):
        return ['id', 'recorded_by', 'cow', 'milking_time', 'gallons']

    @classmethod
    def get_seed_read_keys(cls):
        return ['id', 'seeded_by', 'pasture', 'cereal_hay',
                'grass_hay', 'legume_hay', 'season', 'year', 'link']

    @classmethod
    def get_seed_write_keys(cls):
        return ['id', 'seeded_by', 'pasture', 'cereal_hay',
                'grass_hay', 'legume_hay', 'season', 'year']

    @classmethod
    def get_hr_read_keys(cls):
        return ['id', 'cow', 'recorded_by', 'temperature', 'respiratory_rate',
                'heart_rate', 'blood_pressure', 'weight', 'body_condition_score',
                'illness', 'injury', 'vaccine', 'inspection_time', 'link']

    @classmethod
    def get_hr_write_keys(cls):
        return ['id', 'cow', 'recorded_by', 'temperature', 'respiratory_rate',
                'heart_rate', 'blood_pressure', 'weight', 'body_condition_score',
                'illness', 'injury', 'vaccine', 'inspection_time']

class TestTime:
    @classmethod
    def get_purchase_date(cls):
        return '2014-12-31'

    @classmethod
    def convert_date(cls, d):
        return datetime.strftime(d, '%Y-%m-%d')

    @classmethod
    def convert_datetime(cls, dt):
        return datetime.strftime(dt, '%Y-%m-%d %H:%M:%S.%f+00:00')

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

    @classmethod
    def get_year(cls):
        return 2016
