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
    parser = ArgumentParser(description='Seed pastures for grazing')
    parser.add_argument('-c',
                        '--cereal',
                        type=str,
                        required=False,
                        choices=['alfalfa',
                                 'barley',
                                 'oat',
                                 'rye',
                                 'wheat'],
                        default='alfalfa',
                        help='cereal grain planted to make hay')
    parser.add_argument('-g',
                        '--grass',
                        type=str,
                        required=False,
                        choices=['bermuda',
                                 'bluegrass',
                                 'brome',
                                 'fescue',
                                 'orchardgrass',
                                 'reed canary grass',
                                 'ryegrass',
                                 'sudangrass',
                                 'timothy'],
                        default='timothy',
                        help='grass planted to make hay')
    parser.add_argument('-l',
                        '--legume',
                        type=str,
                        required=False,
                        choices=['clover',
                                 'cowpeas',
                                 'lespedeza',
                                 'soybean',
                                 'trefoil',
                                 'vetch'],
                        default='clover',
                        help='legume planted to make hay')
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
                                 'South East',
                                 'Pen'],
                        help='field region allocation')
    parser.add_argument('-u',
                        '--username',
                        type=str,
                        required=True,
                        help='username of user')
    o = parser.parse_args()
    return(o.cereal,
           o.grass,
           o.legume,
           o.season,
           o.region,
           o.username)
    
def plant_pasture(cereal_hay, grass_hay, legume_hay, season, region, username):
    from django.contrib.auth.models import User
    from assets.models import CerealHay, GrassHay, LegumeHay, RegionImage, Season
    from assets.serializers import PastureSerializer
    try:
        user = User.objects.get(username=username)
        cereal_hay = CerealHay.objects.get(name=cereal_hay)
        grass_hay = GrassHay.objects.get(name=grass_hay)
        legume_hay = LegumeHay.objects.get(name=legume_hay)
        image = RegionImage.objects.get(region__name=region)
        season = Season.objects.get(name=season)
        data = {'seeded_by': user.id,
                'cereal_hay': cereal_hay.id,
                'grass_hay': grass_hay.id,
                'legume_hay': legume_hay.id,
                'season': season.id,
                'image': image.id}
        ps = PastureSerializer(data=data)
        if ps.is_valid() and len(ps.errors) == 0:
            ps.save()
            msg_1 = '{} planted {}, {} '.format(username, cereal_hay.name, grass_hay.name)
            msg_2 = 'and {} in region {} for {} season'.format(legume_hay.name,
                                                               image.region.name,
                                                               season.name)
            print(msg_1 + msg_2) 
            return
        else:
            print('PastureSerializer valid: {}'.format(ps.is_valid()))
            print('PastureSerializer errors: {}'.format(ps.errors))
            print('ERROR: {}'.format(ps.errors))
    except PermissionDenied as e:
        print('PermissionDenied')
        print('ERROR: {}'.format(e))
        print('ERROR: {} unable to seed region {}!'.format(username, region))
        exit(1)
    except IntegrityError as e:
        print('IntegrityError')
        print('ERROR: {}'.format(e))
        exit(1)

def main():
    (cereal_hay, grass_hay, legume_hay, season, region, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    plant_pasture(cereal_hay,
                  grass_hay,
                  legume_hay,
                  season,
                  region,
                  username)
    return

if __name__ == '__main__':
    main()
    exit(0)
