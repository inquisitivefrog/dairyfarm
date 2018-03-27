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
           o.color,
           o.quantity,
           o.date,
           o.username)
    
def _get_data(breed, color, date, user):
    from assets.models import Age, Breed, Cow
    from tools.utils import TestTime
    ages = [ a.name for a in Age.objects.all() ]
    age = ages[randint(0, len(ages) - 1)]
    tmp = []
    for word in breed.split('_'):
       tmp.append(word.capitalize()) 
    b_name = ' '.join(tmp)
    breed = Breed.objects.get(name=b_name)
    return {'rfid': uuid4(),
            'purchased_by': user,
            'purchase_date': TestTime.convert_date(date),
            'color': color,
            'age': age,
            'breed': breed}

def purchase_cow(breed, color, date, username):
    from django.contrib.auth.models import User
    from assets.serializers import CowWriteSerializer
    try:
        user = User.objects.get(username=username)
        cs = CowWriteSerializer(data=_get_data(breed, color, date, user))
        if cs.is_valid() and len(cs.errors) == 0:
            cs.save()
            return
        else:
           print('ERROR: cs errors: {}'.format(cs.errors))
           exit(1)
    except PermissionDenied as e:
        print('ERROR: unable to create username: {}!'.format(username))
        exit(1)
    except IntegrityError as e:
        print('REAL ERROR: {}'.format(str(e)))
        exit(1)

def main():
    (breed, color, quantity, date, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    bought = 0
    for i in range(quantity):
        purchase_cow(breed, color, date, username)
        bought += 1
    if bought == 1:
        print('{} {} {} purchased on {} by {}'.format(bought, color, breed, date, username))
    elif breed.endswith('s'):
        print('{} {} {}es purchased on {} by {}'.format(bought, color, breed, date, username))
    else:
        print('{} {} {}s purchased on {} by {}'.format(bought, color, breed, date, username))
    return

if __name__ == '__main__':
    main()
    exit(0)
