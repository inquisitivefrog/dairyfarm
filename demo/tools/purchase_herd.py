#!/Users/tim/demo/bin/python3

from argparse import ArgumentParser
from os import environ
from random import randint
from sys import exit, path
from uuid import uuid4

from django import setup
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.utils import IntegrityError

def read_args():
    parser = ArgumentParser(description='Purchase a herd of cattle')
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
    parser.add_argument('-q',
                        '--quantity',
                        type=int,
                        required=False,
                        default=10,
                        help='herd size')
    parser.add_argument('-d',
                        '--date',
                        type=str,
                        required=True,
                        help='purchase date as "%Y-%m-%d"')
    parser.add_argument('-u',
                        '--username',
                        type=str,
                        required=True,
                        help='username of user')
    o = parser.parse_args()
    return(o.breed,
           o.quantity,
           o.date,
           o.username)

def _get_colors(breed):
    cows = {'holstein': ['black_white', 'red_white'],
            'jersey': ['brown', 'tawny'],
            'guernsey': ['golden_white'],
            'ayrshire': ['golden_white'],
            'brown_swiss': ['brown', 'gray'],
            'milking_shorthorn': ['red', 'white', 'roan', 'red_white'],
            'dutch_belted': ['black_white']}
    return cows[breed]

def _get_data(breed, color, date, user):
    from assets.models import Age, Breed
    from tools.utils import TestTime
    ages = [ a.name for a in Age.objects.all() ]
    age = ages[randint(0, len(ages) - 1)]
    tmp = []
    for word in breed.split('_'):
       tmp.append(word.capitalize()) 
    b_name = ' '.join(tmp)
    breed = Breed.objects.get(name=b_name)
    return {'purchased_by': user,
            'purchase_date': TestTime.convert_date(date),
            'rfid': uuid4(),
            'age': age,
            'breed': breed.name,
            'color': color}

def purchase_cow(breed, date, username):
    from django.contrib.auth.models import User
    from assets.serializers import CowWriteSerializer
    try:
        user = User.objects.get(username=username)
        for color in _get_colors(breed):
            cs = CowWriteSerializer(data=_get_data(breed, color, date, user))
            if cs.is_valid() and len(cs.errors) == 0:
                cs.save()
            else:
                print('ERROR: cs errors: {}'.format(cs.errors))
                
    except PermissionDenied as e:
        print('ERROR: unable to create username: {}!'.format(username))
    except IntegrityError as e:
        print('REAL ERROR: {}'.format(str(e)))

def main():
    (breed, quantity, date, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    bought = 0
    for i in range(quantity):
        purchase_cow(breed, date, username)
        bought += 1
    print('{} {} purchased on {} by {}'.format(bought, breed, date, username))
    return

if __name__ == '__main__':
    main()
    exit(0)
