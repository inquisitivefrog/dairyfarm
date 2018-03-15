#!/Users/tim/demo/bin/python3

from argparse import ArgumentParser
from os import environ
from random import randint
from sys import exit, path

from django import setup
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.utils import IntegrityError

def read_args():
    parser = ArgumentParser(description='Routine Bovine Behavior of herd')
    parser.add_argument('-b',
                        '--breed',
                        type=str,
                        required=False,
                        choices=['holstein',
                                 'jersey',
                                 'guernsey',
                                 'ayrshire',
                                 'brown_swiss',
                                 'milking_shorthorn',
                                 'dutch_belted'],
                        default='holstein',
                        help='breed of cattle')
    parser.add_argument('-c',
                        '--color',
                        type=str,
                        required=False,
                        choices=['black_white',
                                 'red_white',
                                 'brown',
                                 'tawny',
                                 'golden_white',
                                 'gray',
                                 'red',
                                 'white',
                                 'roan'],
                        default='black_white',
                        help='breed color')
    parser.add_argument('-d',
                        '--date',
                        type=str,
                        required=True,
                        help='inspection time as "%Y-%m-%d"')
    parser.add_argument('-u',
                        '--username',
                        type=str,
                        required=True,
                        help='username of user')
    o = parser.parse_args()
    return(o.breed,
           o.color,
           o.date,
           o.username)
    
def evening_healthy_routine(cow, dt, user):
    from tools.utils import TestData

    data = TestData.get_healthy_cow_data(cow, dt, user)
    TestData.log_healthrecord(data, cow, dt, user)
    TestData.log_event('Get milked', cow, dt, user)
    gallons = randint(5, 7)
    TestData.log_milk(gallons, cow, dt, user)
    TestData.log_event('Sleep', cow, dt, user)
    return

def evening_ill_routine(cow, dt, user):
    from assets.models import Treatment
    from tools.utils import TestData

    data = TestData.get_ill_cow_data(cow, dt, user)
    TestData.log_healthrecord(data, cow, dt, user)
    TestData.log_event('Call Vet', cow, dt, user)
    TestData.log_event('Get diagnosed', cow, dt, user)
    TestData.log_event('Get treated', cow, dt, user)
    treatment_id = randint(1, len(Treatment.objects.all()) - 1)
    treatment = Treatment.objects.get(pk=treatment_id)
    TestData.log_vaccination(treatment.name, cow, dt, user)
    TestData.log_event('Sleep', cow, dt, user)
    return

def evening_injured_routine(cow, dt, user):
    from tools.utils import TestData

    data = TestData.get_injured_cow_data(cow, dt, user)
    TestData.log_healthrecord(data, cow, dt, user)
    TestData.log_event('Call Vet', cow, dt, user)
    TestData.log_event('Get diagnosed', cow, dt, user)
    TestData.log_event('Get treated', cow, dt, user)
    TestData.log_event('Pedicure', cow, dt, user)
    gallons = randint(5, 7)
    TestData.log_milk(gallons, cow, dt, user)
    TestData.log_event('Get milked', cow, dt, user)
    TestData.log_event('Sleep', cow, dt, user)
    return

def morning_healthy_routine(cow, dt, user):
    from assets.models import Pasture
    from tools.utils import TestData

    data = TestData.get_healthy_cow_data(cow, dt, user)
    TestData.log_healthrecord(data, cow, dt, user)
    TestData.log_event('Get milked', cow, dt, user)
    gallons = randint(5, 7)
    TestData.log_milk(gallons, cow, dt, user)
    TestData.log_event('Get milked', cow, dt, user)
    pastures = Pasture.objects.filter(fallow=False)
    pasture = pastures[randint(1, len(pastures) - 1)]
    distance = pasture.id
    TestData.log_exercise(distance, pasture, cow, dt, user)
    TestData.log_event('Walk to pasture', cow, dt, user)
    TestData.log_event('Graze', cow, dt, user)
    TestData.log_event('Drink', cow, dt, user)
    TestData.log_event('Chew cud', cow, dt, user)
    TestData.log_event('Nap', cow, dt, user)
    TestData.log_event('Return to barn', cow, dt, user)
    TestData.log_exercise(distance, pasture, cow, dt, user)
    return

def morning_ill_routine(cow, dt, user):
    from assets.models import Treatment
    from tools.utils import TestData

    data = TestData.get_ill_cow_data(cow, dt, user)
    TestData.log_healthrecord(data, cow, dt, user)
    TestData.log_event('Call Vet', cow, dt, user)
    TestData.log_event('Get diagnosed', cow, dt, user)
    TestData.log_event('Get treated', cow, dt, user)
    treatment_id = randint(1, len(Treatment.objects.all()) - 1)
    treatment = Treatment.objects.get(pk=treatment_id)
    TestData.log_vaccination(treatment.name, cow, dt, user)
    TestData.log_event('Rest in pen', cow, dt, user)
    TestData.log_event('Graze', cow, dt, user)
    TestData.log_event('Drink', cow, dt, user)
    TestData.log_event('Chew cud', cow, dt, user)
    TestData.log_event('Nap', cow, dt, user)
    return

def morning_injured_routine(cow, dt, user):
    from assets.models import Pasture
    from tools.utils import TestData

    data = TestData.get_injured_cow_data(cow, dt, user)
    TestData.log_healthrecord(data, cow, dt, user)
    TestData.log_event('Call Vet', cow, dt, user)
    TestData.log_event('Get diagnosed', cow, dt, user)
    TestData.log_event('Get treated', cow, dt, user)
    gallons = randint(5, 7)
    TestData.log_milk(gallons, cow, dt, user)
    TestData.log_event('Get milked', cow, dt, user)
    TestData.log_event('Exercise in pen', cow, dt, user)
    pasture = Pasture.objects.get(region__name='Pen')
    distance = randint(1, 2)
    TestData.log_exercise(distance, pasture, cow, dt, user)
    TestData.log_event('Graze', cow, dt, user)
    TestData.log_event('Drink', cow, dt, user)
    TestData.log_event('Chew cud', cow, dt, user)
    TestData.log_event('Nap', cow, dt, user)
    return

def daily_routine(cow, date, user, first=False):
    from assets.models import Pasture, Treatment
    from tools.utils import TestData, TestTime

    # morning
    dt = TestTime.get_morning(date)
    TestData.log_event('Wake Up', cow, dt, user)
    TestData.log_event('Get inspected', cow, dt, user)
    if first:
        health = 'healthy'
    else:
        health = TestData.get_health()
    if health == 'healthy':
        morning_healthy_routine(cow, dt, user)
    elif health == 'injured':
        morning_injured_routine(cow, dt, user)
    elif health == 'ill':
        morning_ill_routine(cow, dt, user)

    # evening
    dt = TestTime.get_evening(date)
    TestData.log_event('Get inspected', cow, dt, user)
    if first:
        health = 'healthy'
    else:
        health = TestData.get_health()
    if health == 'healthy':
        evening_healthy_routine(cow, dt, user)
    elif health == 'injured':
        evening_injured_routine(cow, dt, user)
    elif health == 'ill':
        evening_ill_routine(cow, dt, user)
    return

def main():
    (breed, color, date, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    from django.contrib.auth.models import User
    from assets.models import Cow
    from tools.utils import TestData, TestTime
    user = User.objects.get(username=username)
    inspected = 0
    for cow in Cow.objects.filter(breed__name=TestData.convert_name(breed),
                                  color__name=color):
        if inspected > 0:
            daily_routine(cow, date, user)
        else:
            daily_routine(cow, date, user, first=True)
        inspected += 1
    if inspected == 1:
        print('{} inspected {} {}'.format(username, inspected, breed))
    else:
        print('{} inspected {} {}s'.format(username, inspected, breed))
    return

if __name__ == '__main__':
    main()
    exit(0)
