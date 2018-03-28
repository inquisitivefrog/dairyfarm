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
    parser.add_argument('-p',
                        '--pasture',
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
                        help='which pasture to seed')
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
    return(o.cereal,
           o.grass,
           o.legume,
           o.pasture,
           o.season,
           o.username,
           o.year)
    
def _convert_name(n):
    prefix = '/static/images/regions/'
    suffix = '.png'
    words = []
    for word in n.split():
        words.append(word.lower())
    new_word = '_'.join(words)
    return prefix + new_word + suffix

def _get_data(cereal_hay, grass_hay, legume_hay, pasture, season, username, year):
    from django.contrib.auth.models import User
    from tools.utils import TestTime
    user = User.objects.get(username=username)
    return {'seeded_by': username,
            'cereal_hay': cereal_hay,
            'year': year,
            'season': season,
            'grass_hay': grass_hay,
            'legume_hay': legume_hay,
            'pasture': pasture}

def plant_pasture(cereal_hay, grass_hay, legume_hay, pasture, season, username, year):
    from assets.serializers import SeedWriteSerializer
    try:
        ss = SeedWriteSerializer(data=_get_data(cereal_hay, grass_hay, legume_hay,
                                                pasture, season, username, year))
        if ss.is_valid() and len(ss.errors) == 0:
            ss.save()
            msg_1 = '{} planted {}, {} '.format(username, cereal_hay, grass_hay)
            msg_2 = 'and {} in region {} for {} {}'.format(legume_hay,
                                                           pasture,
                                                           season,
                                                           year)
            print(msg_1 + msg_2) 
            return
        else:
            print('ERROR: {}'.format(ss.errors))
    except PermissionDenied as e:
        print('PermissionDenied')
        print('ERROR: {}'.format(e))
        print('ERROR: {} unable to seed pasture {}!'.format(username, pasture))
        exit(1)
    except IntegrityError as e:
        print('IntegrityError')
        print('ERROR: {}'.format(e))
        exit(1)

def main():
    (cereal_hay, grass_hay, legume_hay, pasture, season, username, year) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    plant_pasture(cereal_hay,
                  grass_hay,
                  legume_hay,
                  pasture,
                  season,
                  username,
                  year)
    return

if __name__ == '__main__':
    main()
    exit(0)
