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
    parser.add_argument('-d',
                        '--datetime',
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
           o.datetime,
           o.username)
    
def evening_healthy_routine(c_id, dt, u_id):
    from tools.utils import TestData

    data = TestData.get_healthy_cow_data(c_id, dt, u_id)
    TestData.log_healthrecord(data, c_id, dt, u_id)
    TestData.log_event('Get milked', c_id, dt, u_id)
    gallons = randint(5, 7)
    TestData.log_milk(gallons, c_id, dt, u_id)
    TestData.log_event('Sleep', c_id, dt, u_id)
    return

def evening_ill_routine(c_id, dt, u_id):
    from assets.models import Treatment
    from tools.utils import TestData

    data = TestData.get_ill_cow_data(c_id, dt, u_id)
    TestData.log_healthrecord(data, c_id, dt, u_id)
    TestData.log_event('Call Vet', c_id, dt, u_id)
    TestData.log_event('Get diagnosed', c_id, dt, u_id)
    TestData.log_event('Get treated', c_id, dt, u_id)
    treatment_id = randint(1, len(Treatment.objects.all()) - 1)
    treatment = Treatment.objects.get(pk=treatment_id)
    TestData.log_vaccination(treatment.name, c_id, dt, u_id)
    TestData.log_event('Sleep', c_id, dt, u_id)
    return

def evening_injured_routine(c_id, dt, u_id):
    from tools.utils import TestData

    data = TestData.get_injured_cow_data(c_id, dt, u_id)
    TestData.log_healthrecord(data, c_id, dt, u_id)
    TestData.log_event('Call Vet', c_id, dt, u_id)
    TestData.log_event('Get diagnosed', c_id, dt, u_id)
    TestData.log_event('Get treated', c_id, dt, u_id)
    TestData.log_event('Pedicure', c_id, dt, u_id)
    gallons = randint(5, 7)
    TestData.log_milk(gallons, c_id, dt, u_id)
    TestData.log_event('Get milked', c_id, dt, u_id)
    TestData.log_event('Sleep', c_id, dt, u_id)
    return

def morning_healthy_routine(c_id, dt, u_id):
    from assets.models import Pasture
    from tools.utils import TestData

    data = TestData.get_healthy_cow_data(c_id, dt, u_id)
    TestData.log_healthrecord(data, c_id, dt, u_id)
    TestData.log_event('Get milked', c_id, dt, u_id)
    gallons = randint(5, 7)
    TestData.log_milk(gallons, c_id, dt, u_id)
    TestData.log_event('Get milked', c_id, dt, u_id)
    pastures = Pasture.objects.all()
    p_id = randint(1, len(pastures) - 2)
    distance = p_id
    TestData.log_exercise(distance, p_id, c_id, dt, u_id)
    TestData.log_event('Walk to pasture', c_id, dt, u_id)
    TestData.log_event('Graze', c_id, dt, u_id)
    TestData.log_event('Drink', c_id, dt, u_id)
    TestData.log_event('Chew cud', c_id, dt, u_id)
    TestData.log_event('Nap', c_id, dt, u_id)
    TestData.log_event('Return to barn', c_id, dt, u_id)
    TestData.log_exercise(distance, p_id, c_id, dt, u_id)
    return

def morning_ill_routine(c_id, dt, u_id):
    from assets.models import Treatment
    from tools.utils import TestData

    data = TestData.get_ill_cow_data(c_id, dt, u_id)
    TestData.log_healthrecord(data, c_id, dt, u_id)
    TestData.log_event('Call Vet', c_id, dt, u_id)
    TestData.log_event('Get diagnosed', c_id, dt, u_id)
    TestData.log_event('Get treated', c_id, dt, u_id)
    treatment_id = randint(1, len(Treatment.objects.all()) - 1)
    treatment = Treatment.objects.get(pk=treatment_id)
    TestData.log_vaccination(treatment.name, c_id, dt, u_id)
    TestData.log_event('Rest in pen', c_id, dt, u_id)
    TestData.log_event('Graze', c_id, dt, u_id)
    TestData.log_event('Drink', c_id, dt, u_id)
    TestData.log_event('Chew cud', c_id, dt, u_id)
    TestData.log_event('Nap', c_id, dt, u_id)
    return

def morning_injured_routine(c_id, dt, u_id):
    from assets.models import Pasture
    from tools.utils import TestData

    data = TestData.get_injured_cow_data(c_id, dt, u_id)
    TestData.log_healthrecord(data, c_id, dt, u_id)
    TestData.log_event('Call Vet', c_id, dt, u_id)
    TestData.log_event('Get diagnosed', c_id, dt, u_id)
    TestData.log_event('Get treated', c_id, dt, u_id)
    gallons = randint(5, 7)
    TestData.log_milk(gallons, c_id, dt, u_id)
    TestData.log_event('Get milked', c_id, dt, u_id)
    TestData.log_event('Exercise in pen', c_id, dt, u_id)
    p_id = Pasture.objects.get(image__region__name='Pen').id
    distance = randint(1, 2)
    TestData.log_exercise(distance, p_id, c_id, dt, u_id)
    TestData.log_event('Graze', c_id, dt, u_id)
    TestData.log_event('Drink', c_id, dt, u_id)
    TestData.log_event('Chew cud', c_id, dt, u_id)
    TestData.log_event('Nap', c_id, dt, u_id)
    return

def daily_routine(c_id, dt, u_id):
    from assets.models import Pasture, Treatment
    from tools.utils import TestData

    # morning
    TestData.log_event('Wake Up', c_id, dt, u_id)
    TestData.log_event('Get inspected', c_id, dt, u_id)
    health = TestData.get_health()
    if health == 'healthy':
        morning_healthy_routine(c_id, dt, u_id)
    elif health == 'injured':
        morning_injured_routine(c_id, dt, u_id)
    elif health == 'ill':
        morning_ill_routine(c_id, dt, u_id)

    # evening
    TestData.log_event('Get inspected', c_id, dt, u_id)
    health = TestData.get_health()
    if health == 'healthy':
        evening_healthy_routine(c_id, dt, u_id)
    elif health == 'injured':
        evening_injured_routine(c_id, dt, u_id)
    elif health == 'ill':
        evening_ill_routine(c_id, dt, u_id)
    return

def main():
    (breed, datetime, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    from django.contrib.auth.models import User
    from assets.models import Cow
    from tools.utils import TestTime
    user = User.objects.get(username=username)
    dt = TestTime.convert_datetime(datetime)
    new_breed = []
    for word in breed.split('_'):
        new_breed.append(word.capitalize())
    inspected = 0
    for cow in Cow.objects.filter(image__breed__name=' '.join(new_breed)):
        daily_routine(cow.id, dt, user.id)
        inspected += 1
    if inspected == 1:
        print('{} inspected {} {}'.format(username, inspected, breed))
    else:
        print('{} inspected {} {}s'.format(username, inspected, breed))
    return

if __name__ == '__main__':
    main()
    exit(0)
