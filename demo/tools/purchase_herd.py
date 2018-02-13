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
                        '--count',
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
           o.count,
           o.date,
           o.username)
    
def _get_data(breed, date, user):
    from assets.models import Age, Breed, BreedImage, Color
    from tools.utils import TestTime
    ages = [a.id for a in Age.objects.all() ]
    age_id = ages[randint(0, len(ages) - 1)]
    breed_id = Breed.objects.get(name=breed).id
    colors = [ c.id for c in Color.objects.filter(breed=breed_id) ]
    color_id = colors[randint(0, len(colors) - 1)]
    images = [ bi.id for bi in BreedImage.objects.filter(breed=breed_id) ]
    image_id = images[randint(0, len(images) - 1)]
    return {'purchased_by': user.id,
            'purchase_date': TestTime.convert_date(date),
            'color': color_id,
            'age': age_id,
            'image': image_id}

def purchase_cow(breed, date, username):
    from django.contrib.auth.models import User
    from assets.serializers import CowSerializer
    try:
        user = User.objects.get(username=username)
        cs = CowSerializer(data=_get_data(breed, date, user))
        if cs.is_valid() and len(cs.errors) == 0:
            cs.save()
            return
        else:
           print('ERROR: {}'.format(cs.errors))
    except PermissionDenied as e:
        print('ERROR: unable to create username: {}!'.format(username))
        exit(1)
    except IntegrityError as e:
        print('ERROR: username: {} already exists!'.format(username))
        exit(1)

def main():
    (breed, count, date, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    bought = 0
    for i in range(count):
        new_breed = []
        for word in breed.split('_'):
            new_breed.append(word.capitalize())
        purchase_cow(' '.join(new_breed), date, username)
        bought += 1
    if bought == 1:
        print('{} purchased {} {}'.format(username, bought, breed))
    else:
        print('{} purchased {} {}s'.format(username, bought, breed))
    return

if __name__ == '__main__':
    main()
    exit(0)