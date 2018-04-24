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
    from tools.utils import ToolData

    data = ToolData.get_healthy_cow_data(cow, dt, user)
    ToolData.log_healthrecord(data, cow, dt, user)
    ToolData.log_event('Get milked', cow, dt, user)
    gallons = randint(5, 7)
    ToolData.log_milk(gallons, cow, dt, user)
    ToolData.log_event('Sleep', cow, dt, user)
    return

def evening_ill_routine(cow, dt, user):
    from assets.models import Vaccine
    from tools.utils import ToolData

    data = ToolData.get_ill_cow_data(cow, dt, user)
    ToolData.log_healthrecord(data, cow, dt, user)
    ToolData.log_event('Call Vet', cow, dt, user)
    ToolData.log_event('Get diagnosed', cow, dt, user)
    ToolData.log_event('Get treated', cow, dt, user)
    ToolData.log_event('Sleep', cow, dt, user)
    return

def evening_injured_routine(cow, dt, user):
    from tools.utils import ToolData

    data = ToolData.get_injured_cow_data(cow, dt, user)
    ToolData.log_healthrecord(data, cow, dt, user)
    ToolData.log_event('Call Vet', cow, dt, user)
    ToolData.log_event('Get diagnosed', cow, dt, user)
    ToolData.log_event('Get treated', cow, dt, user)
    ToolData.log_event('Pedicure', cow, dt, user)
    gallons = randint(5, 7)
    ToolData.log_milk(gallons, cow, dt, user)
    ToolData.log_event('Get milked', cow, dt, user)
    ToolData.log_event('Sleep', cow, dt, user)
    return

def morning_healthy_routine(cow, dt, user):
    from assets.models import Pasture
    from tools.utils import ToolData

    data = ToolData.get_healthy_cow_data(cow, dt, user)
    ToolData.log_healthrecord(data, cow, dt, user)
    ToolData.log_event('Get milked', cow, dt, user)
    gallons = randint(5, 7)
    ToolData.log_milk(gallons, cow, dt, user)
    ToolData.log_event('Get milked', cow, dt, user)
    # dt should be 1-90d > plant_date but will vary by season due to uneven calendar
    pastures = Pasture.objects.filter(fallow=False)
    pasture = pastures[randint(1, len(pastures) - 1)]
    ToolData.log_exercise(pasture, cow, dt, user)
    ToolData.log_event('Walk to pasture', cow, dt, user)
    ToolData.log_event('Graze', cow, dt, user)
    ToolData.log_event('Drink', cow, dt, user)
    ToolData.log_event('Chew cud', cow, dt, user)
    ToolData.log_event('Nap', cow, dt, user)
    ToolData.log_event('Return to barn', cow, dt, user)
    ToolData.log_exercise(pasture, cow, dt, user)
    return

def morning_ill_routine(cow, dt, user):
    from assets.models import Vaccine
    from tools.utils import ToolData

    data = ToolData.get_ill_cow_data(cow, dt, user)
    ToolData.log_healthrecord(data, cow, dt, user)
    ToolData.log_event('Call Vet', cow, dt, user)
    ToolData.log_event('Get diagnosed', cow, dt, user)
    ToolData.log_event('Get treated', cow, dt, user)
    ToolData.log_event('Rest in pen', cow, dt, user)
    ToolData.log_event('Graze', cow, dt, user)
    ToolData.log_event('Drink', cow, dt, user)
    ToolData.log_event('Chew cud', cow, dt, user)
    ToolData.log_event('Nap', cow, dt, user)
    return

def morning_injured_routine(cow, dt, user):
    from assets.models import Pasture
    from tools.utils import ToolData

    data = ToolData.get_injured_cow_data(cow, dt, user)
    ToolData.log_healthrecord(data, cow, dt, user)
    ToolData.log_event('Call Vet', cow, dt, user)
    ToolData.log_event('Get diagnosed', cow, dt, user)
    ToolData.log_event('Get treated', cow, dt, user)
    gallons = randint(5, 7)
    ToolData.log_milk(gallons, cow, dt, user)
    ToolData.log_event('Get milked', cow, dt, user)
    ToolData.log_event('Exercise in pen', cow, dt, user)
    pasture = Pasture.objects.get(name='Pen')
    ToolData.log_exercise(pasture, cow, dt, user)
    ToolData.log_event('Graze', cow, dt, user)
    ToolData.log_event('Drink', cow, dt, user)
    ToolData.log_event('Chew cud', cow, dt, user)
    ToolData.log_event('Nap', cow, dt, user)
    return

def daily_routine(cow, date, user, first=False):
    from assets.models import Pasture, Treatment
    from tools.utils import ToolData, ToolTime

    # morning
    dt = ToolTime.get_morning(date)
    ToolData.log_event('Wake Up', cow, dt, user)
    ToolData.log_event('Get inspected', cow, dt, user)
    if first:
        health = 'healthy'
    else:
        health = ToolData.get_health()
    if health == 'healthy':
        morning_healthy_routine(cow, dt, user)
    elif health == 'injured':
        morning_injured_routine(cow, dt, user)
    elif health == 'ill':
        morning_ill_routine(cow, dt, user)

    # evening
    dt = ToolTime.get_evening(date)
    ToolData.log_event('Get inspected', cow, dt, user)
    if first:
        health = 'healthy'
    else:
        health = ToolData.get_health()
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
    from tools.utils import ToolData, ToolTime
    user = User.objects.get(username=username)
    inspected = 0
    for cow in Cow.objects.filter(breed__name=ToolData.convert_name(breed),
                                  color__name=color):
        if inspected > 0:
            daily_routine(cow, date, user)
        else:
            daily_routine(cow, date, user, first=True)
        inspected += 1
    if inspected == 1:
        print('{} {} inspected on {} by {}'.format(inspected, breed, date, username))
    elif breed.endswith('s'):
        print('{} {} inspected on {} by {}'.format(inspected, breed, date, username))
    else:
        print('{} {}s inspected on {} by {}'.format(inspected, breed, date, username))
    return

if __name__ == '__main__':
    main()
    exit(0)
