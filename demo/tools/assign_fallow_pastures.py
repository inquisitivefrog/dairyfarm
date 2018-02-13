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
    parser.add_argument('-s',
                        '--season',
                        type=str,
                        required=True,
                        choices=['Spring',
                                 'Summer',
                                 'Autumn',
                                 'Winter'],
                        help='planting season')
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
                                 'South East'],
                        help='field region allocation')
    parser.add_argument('-u',
                        '--username',
                        type=str,
                        required=True,
                        help='username of user')
    o = parser.parse_args()
    return(o.season,
           o.region,
           o.username)
    
def leave_fallow(season, region, username):
    from django.contrib.auth.models import User
    from assets.models import Pasture, RegionImage, Season
    from assets.serializers import PastureSerializer
    try:
        user = User.objects.get(username=username)
        distance = randint(1, 12)
        season = Season.objects.get(name=season)
        image = RegionImage.objects.get(region__name=region)
        instance = Pasture.objects.get(seeded_by=user.id,
                                       season=season.id,
                                       image=image.id)
        data = {'seeded_by': user.id,
                'distance': distance,
                'fallow': True,
                'cereal_hay': None,
                'grass_hay': None,
                'legume_hay': None,
                'season': season.id,
                'image': image.id}
        ps = PastureSerializer(instance,
                               data=data,
                               partial=True)
        if ps.is_valid() and len(ps.errors) == 0:
            ps.save()
            print('Region {} left fallow for {} season by {}'.format(image.region.name,
                                                                     season.name,
                                                                     username))
            return
        else:
            print('ERROR: {}'.format(ps.errors))
    except PermissionDenied as e:
        print('ERROR: {}'.format(e))
        print('ERROR: {} unable to create pasture!'.format(username))
        exit(1)
    except IntegrityError as e:
        print('ERROR: {}'.format(e))
        exit(1)

def main():
    (season, meadow, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    leave_fallow(season,
                 meadow,
                 username)
    return

if __name__ == '__main__':
    main()
    exit(0)
