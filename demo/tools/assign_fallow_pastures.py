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
    parser = ArgumentParser(description='Leave pastures fallow to recover nutrients')
    parser.add_argument('-r',
                        '--region',
                        type=str,
                        required=True,
                        choices=['North',
                                 'West',
                                 'South',
                                 'East',
                                 'Central North',
                                 'Central West',
                                 'Central South',
                                 'Central East',
                                 'North West',
                                 'North East',
                                 'South West',
                                 'South East',
                                 'Pen'],
                        help='field region allocation')
    parser.add_argument('-s',
                        '--season',
                        type=str,
                        choices=['Spring', 'Summer', 'Autumn', 'Winter'],
                        required=True,
                        help='season planted')
    parser.add_argument('-u',
                        '--username',
                        type=str,
                        required=True,
                        help='username of user')
    parser.add_argument('-y',
                        '--year',
                        type=int,
                        required=True,
                        help='year planted YYYY')
    o = parser.parse_args()
    return(o.region,
           o.season,
           o.username,
           o.year)
    
def _get_instance(region, season, user, year):
    from assets.models import Pasture, Region, Season
    from tools.utils import TestTime
    try:
        r_id = Region.objects.get(name=region).id
        s_id = Season.objects.get(name=season).id
        instance = Pasture.objects.get(seeded_by=user,
                                       season=s_id,
                                       year=year,
                                       region=r_id)
        return instance
    except Pasture.DoesNotExist as e:
        print('ERROR: pasture not seeded')
        exit(1)

def _get_data():
    return {'distance': randint(1, 2),
            'fallow': True}

def leave_fallow(region, season, username, year):
    from django.contrib.auth.models import User
    from assets.models import Pasture
    from assets.serializers import PastureSerializer

    try:
        user = User.objects.get(username=username)
        ps = PastureSerializer(instance=_get_instance(region, season, user, year),
                               data=_get_data(),
                               partial=True)
        if ps.is_valid() and len(ps.errors) == 0:
            ps.save()
            print('Region {} left fallow for {} {} by {}'.format(region,
                                                                 season,
                                                                 year,
                                                                 username))
            return
        else:
            print('ERROR: {}'.format(ps.errors))
            exit(1)
    except PermissionDenied as e:
        print('ERROR: {}'.format(e))
        print('ERROR: {} unable to make pasture fallow!'.format(username))
        exit(1)
    except IntegrityError as e:
        print('ERROR: {}'.format(e))
        exit(1)

def main():
    (region, season, username, year) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    leave_fallow(region,
                 season,
                 username,
                 year)
    return

if __name__ == '__main__':
    main()
    exit(0)
