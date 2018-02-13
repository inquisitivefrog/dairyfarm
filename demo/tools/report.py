#!/Users/tim/demo/bin/python3

from argparse import ArgumentParser
from os import environ
from random import randint
from sys import exit, path

from django import setup
from django.conf import settings

def read_args():
    parser = ArgumentParser(description='health records report')
    parser.add_argument('-d',
                        '--debug',
                        required=False,
                        action='store_true',
                        default=False,
                        help='display more information')
    o = parser.parse_args()
    return (o.debug)

def _debug_info(low, high, stat):
    if len(low) > 0:
        print('DEBUG: low_{}: {}'.format(stat, low))
    if len(high) > 0:
        print('DEBUG: high_{}: {}'.format(stat, high))
    return

def get_temp_stats(debug=False):
    from assets.models import HealthRecord
    # ideal healthy temperature range: 100.4 - 102.0
    low_temp = [ x.temperature for x in HealthRecord.objects.filter(temperature__lt=100.4) ]
    high_temp = [ x.temperature for x in HealthRecord.objects.filter(temperature__gt=102.0) ]
    if debug:
        _debug_info(low_temp, high_temp, 'temp')
    return (len(low_temp), len(high_temp))

def get_resp_stats(debug=False):
    from assets.models import HealthRecord
    # ideal healthy respiratory_rate range: 26 - 50
    low_resp = [ x.respiratory_rate for x in HealthRecord.objects.filter(respiratory_rate__lt=26.0) ]
    high_resp = [ x.respiratory_rate for x in HealthRecord.objects.filter(respiratory_rate__gt=50.0) ]
    if debug:
        _debug_info(low_resp, high_resp, 'resp')
    return (len(low_resp), len(high_resp))

def get_hr_stats(debug=False):
    from assets.models import HealthRecord
    # ideal healthy heart_rate range: 48 - 84
    low_hr = [ x.heart_rate for x in HealthRecord.objects.filter(heart_rate__lt=48.0) ]
    high_hr = [ x.heart_rate for x in HealthRecord.objects.filter(heart_rate__gt=84.0) ]
    if debug:
        _debug_info(low_hr, high_hr, 'HR')
    return (len(low_hr), len(high_hr))

def get_bp_stats():
    from assets.models import HealthRecord
    # ideal healthy BP range: 130 - 150
    low_bp = len(HealthRecord.objects.filter(blood_pressure__lt=130.0))
    high_bp = len(HealthRecord.objects.filter(blood_pressure__gt=150.0))
    return (low_bp, high_bp)

def get_bcs_stats():
    from assets.models import HealthRecord
    # ideal healthy BCS range: 3.0 - 3.5
    low_bcs = len(HealthRecord.objects.filter(body_condition_score__lt=3.0))
    high_bcs = len(HealthRecord.objects.filter(body_condition_score__gt=3.5))
    return (low_bcs, high_bcs)

def get_stats(debug):
    from assets.models import HealthRecord
    total = len(HealthRecord.objects.all())
    healthy = len(HealthRecord.objects.filter(status_id__in=[1,2]))
    injured = len(HealthRecord.objects.filter(status_id=3))
    ill = len(HealthRecord.objects.filter(status_id__in=[4,5]))
    return ({'total': total,
             'healthy': healthy,
             'injured': injured,
             'ill': ill},
            {'temperature': get_temp_stats(debug=debug),
             'respiratory': get_resp_stats(debug=debug),
             'HR': get_hr_stats(debug=debug),
             'BP': get_bp_stats(),
             'BCS': get_bcs_stats()})

def _format(key):
    while len(key) != 4:
        key += ' '
    return key
        
def display_records():
    from assets.models import Action, Age, Breed, BreedImage, CerealHay
    from assets.models import Color, Cow, GrassHay, Illness
    from assets.models import Injury, LegumeHay, Region, RegionImage
    from assets.models import Season, Status, Treatment, Vaccine
    from assets.models import Event, Exercise, HealthRecord, Milk, Pasture
    print('REFERENCES LOADED')
    a = Action.objects.all()
    print('Total Actions: {}'.format(len(a)))
    a = Age.objects.all()
    print('Total Ages: {}'.format(len(a)))
    b = Breed.objects.all()
    print('Total Breeds: {}'.format(len(b)))
    b = BreedImage.objects.all()
    print('Total Breed Images: {}'.format(len(b)))
    c = CerealHay.objects.all()
    print('Total Cereal Hays: {}'.format(len(c)))
    c = Color.objects.all()
    print('Total Colors: {}'.format(len(c)))
    g = GrassHay.objects.all()
    print('Total Grass Hays: {}'.format(len(g)))
    i = Illness.objects.all()
    print('Total Illness types: {}'.format(len(i)))
    i = Injury.objects.all()
    print('Total Injury types: {}'.format(len(i)))
    l = LegumeHay.objects.all()
    print('Total Legume Hays: {}'.format(len(l)))
    r = Region.objects.all()
    print('Total Regions: {}'.format(len(r)))
    i = RegionImage.objects.all()
    print('Total Region images: {}'.format(len(i)))
    s = Season.objects.all()
    print('Total Seasons: {}'.format(len(s)))
    s = Status.objects.all()
    print('Total Statuses: {}'.format(len(s)))
    t = Treatment.objects.all()
    print('Total Treatment types: {}'.format(len(t)))
    v = Vaccine.objects.all()
    print('Total Vaccine types: {}'.format(len(v)))
    return
    
def display_activity():
    from assets.models import Cow, Event, Exercise, HealthRecord, Milk, Pasture
    print('\nRECENT ACTIVITY')
    c = Cow.objects.all()
    print('Total Cows: {} purchased'.format(len(c)))
    e = Event.objects.all()
    print('Total Events: {} logged'.format(len(e)))
    e = Exercise.objects.all()
    print('Total Exercises: {} logged'.format(len(e)))
    hr = HealthRecord.objects.all()
    print('Total Health Records: {} recorded'.format(len(hr)))
    m = Milk.objects.all()
    print('Total gallons of Milk: {} collected'.format(len(m)))
    p = Pasture.objects.filter(fallow=False)
    print('Total Pastures: {} available for grazing'.format(len(p)))
    return

def display_stats(stats):
    print('\nSTATISTICS')
    (major, minor) = stats
    for key, value in major.items():
        print('{}: {}'.format(key, value))
    for key, value in minor.items():
        (low, high) = value
        print(key.upper())
        print('too low: {}'.format(low))
        print('too high: {}'.format(high))
    return

def main():
    debug = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    display_records()
    display_activity()
    display_stats(get_stats(debug))
    return

if __name__ == '__main__':
    main()
    exit(0)
