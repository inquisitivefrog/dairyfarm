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
    parser.add_argument('-u',
                        '--username',
                        type=str,
                        required=True,
                        help='username of user')
    o = parser.parse_args()
    return(o.breed,
           o.count,
           o.username)
    
def _get_attrs(breed):
    from assets.models import Age, Breed, Color, Image
    ages = [a.id for a in Age.objects.all() ]
    a_guess = ages[randint(0, len(ages) - 1)]
    breed_id = Breed.objects.get(name=breed).id
    colors = [ c.id for c in Color.objects.filter(breed=breed_id) ]
    c_guess = colors[randint(0, len(colors) - 1)]
    images = [ i.id for i in Image.objects.filter(breed=breed_id) ]
    i_guess = images[randint(0, len(images) - 1)]
    return (breed_id, c_guess, a_guess, i_guess)

def purchase_cow(breed, username):
    from django.contrib.auth.models import User
    from assets.serializers import CowSerializer
    (breed_id, color_id, age_id, image_id) = _get_attrs(breed)
    try:
        user = User.objects.get(username=username)
        data = {'purchased_by': user.id,
                'breed': breed_id,
                'color': color_id,
                'age': age_id,
                'image': image_id}
        cs = CowSerializer(data=data)
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
    (breed, count, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    bought = 0
    for i in range(count):
        new_breed = []
        for word in breed.split('_'):
            new_breed.append(word.capitalize())
        purchase_cow(' '.join(new_breed), username)
        bought += 1
    if bought == 1:
        print('{} purchased {} {}'.format(username, bought, breed))
    else:
        print('{} purchased {} {}s'.format(username, bought, breed))
    return

if __name__ == '__main__':
    main()
    exit(0)
