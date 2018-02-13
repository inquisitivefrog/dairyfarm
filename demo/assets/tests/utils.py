from random import randint

from django.utils.timezone import datetime, localtime, pytz

def get_action():
    return 'Burp'

def get_breed():
    return 'Criollo'

def get_cereal():
    return 'maize'

def get_grass():
    return 'quackgrass'

def get_illness():
    return 'mad cow'

def get_injury():
    return 'tipped over'

def get_legume():
    return 'sainfoin'

def get_purchase_date():
    return '2014-12-31'

def get_region():
    return 'Dead Center'

def get_regionimage():
    return '/static/images/breeds/belgian_blue.png'

def get_pasture():
    return 'Hill'

def get_season():
    return 'Fall'

def get_status():
    return 'Retired'

def get_treatment():
    return 'apply heating pad'

def get_vaccine():
    return 'cow pox vaccine'

def convert_date(t):
    return datetime.strftime(t, '%Y-%m-%d')

def get_date():
    t = datetime.now()
    return datetime.date(t)

def get_datetime():
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

def get_random_age():
    age = randint(6, 10)
    return '{} years'.format(age)

def get_random_breed():
    breeds = ['Criollo', 'Pineywood', 'Randall', 'Belgian Blue',
              'American Milking Devon', 'Guzerat', 'Red Sindhi']
    breed = randint(0, len(breeds) - 1)
    return breeds[breed]

def get_random_color():
    colors = ['Blue', 'Green', 'Orange', 'Yellow']
    color = randint(0, len(colors) - 1)
    return colors[color]

def get_random_image():
    images = ['/static/images/criollo.png',
              '/static/images/pineywood.png',
              '/static/images/randall.png',
              '/static/images/belgian_blue.png',
              '/static/images/american_milking_devon.png',
              '/static/images/guzerat.png',
              '/static/images/red_sindhi.png']
    image = randint(0, len(images) - 1)
    return images[image]

def get_random_user():
    return 'farmhand'

def get_temp():
    # ideal healthy temp range: 100.4 - 102.0
    return randint(1004, 1020) * 10.0 / 100

def get_resp():
    # ideal healthy resp range: 26 - 50
    return randint(260, 500) * 10.0 / 100

def get_hr():
    # ideal healthy HR range: 48 - 84
    return randint(480, 840) * 10.0 / 100

def get_bp():
    # ideal healthy BP range: 130 - 150
    return randint(1300, 1500) * 10.0 / 100

def get_bcs():
    # ideal healthy BCS range: 3.0 - 3.5
    return randint(30, 35) * 10.0 / 100

def get_weight():
    # ideal healthy weight range: 450 - 550
    return randint(450, 550)
