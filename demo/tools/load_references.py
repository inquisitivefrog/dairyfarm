#!/Users/tim/demo/bin/python3

from os import environ
from sys import exit, path

from django import setup
from django.conf import settings

def load_ages():
    from assets.serializers import AgeSerializer
    ages = ['1 year', '2 years', '3 years', '4 years', '5 years']
    for age in ages:
        data = {'name': age}
        s = AgeSerializer(data=data)
        if s.is_valid() and len(s.errors) == 0:
            print('Defined age: {}'.format(age))
            s.save()
        else:
            if s.errors['name'][0] == 'age with this name already exists.':
                print('WARN: age: {} already defined'.format(age))
            else:
                print('ERROR: {}'.format(s.errors))
    return

def load_breeds():
    from assets.serializers import BreedSerializer
    breeds = ['Holstein', 'Jersey', 'Guernsey', 'Ayrshire',
              'Brown Swiss', 'Milking Shorthorn', 'Dutch Belted']
    for breed in breeds: 
        data = {'name': breed}
        bs = BreedSerializer(data=data)
        if bs.is_valid() and len(bs.errors) == 0:
            print('Defined breed: {}'.format(breed))
            bs.save()
        else:
            if bs.errors['name'][0] == 'breed with this name already exists.':
                print('WARN: breed: {} already defined'.format(breed))
            else:
                print('ERROR: {}'.format(bs.errors))
    return

def load_colors():
    from assets.models import Breed
    from assets.serializers import ColorSerializer
    colors = {'Holstein': ['black_white', 'red_white'],
              'Jersey': ['brown', 'tawny'],
              'Guernsey': ['golden_white'],
              'Ayrshire': ['golden_white'],
              'Brown Swiss': ['brown', 'gray'],
              'Milking Shorthorn': ['red', 'white', 'roan', 'red_white'],
              'Dutch Belted': ['black_white']}
    for breed in colors: 
        for color in colors[breed]:
            data = {'breed': Breed.objects.get(name=breed).id,
                    'name': color}
            cs = ColorSerializer(data=data)
            if cs.is_valid() and len(cs.errors) == 0:
                print('Defined color: {} for breed: {}'.format(color, breed))
                cs.save()
            else:
                if cs.errors['name'][0] == 'color with this name already exists.':
                    print('WARN: color: {} for breed: {} already defined'.format(color, breed))
                else:
                    print('ERROR: {}'.format(cs.errors))
    return

def load_images():
    from assets.models import Breed
    from assets.serializers import ImageSerializer
    images = {'Holstein': '/static/images/holstein.png',
              'Jersey': '/static/images/jersey.png',
              'Guernsey': '/static/images/guernsey.png',
              'Ayrshire': '/static/images/ayrshire.png',
              'Brown Swiss': '/static/images/brown_swiss.png',
              'Milking Shorthorn': '/static/images/milking_shorthorn.png',
              'Dutch Belted': '/static/images/dutch_belted.png'}
    for breed, url in images.items(): 
        data = {'breed': Breed.objects.get(name=breed).id,
                'url': url}
        s = ImageSerializer(data=data)
        if s.is_valid() and len(s.errors) == 0:
            print('Defined image: {} for breed: {}'.format(url, breed))
            s.save()
        else:
            print('ERRORS: {}'.format(s.errors))
            if s.errors['url'][0] == 'image with this url already exists.':
                print('WARN: image: {} for breed: {} already defined'.format(image, breed))
            else:
                print('ERROR: {}'.format(s.errors))
    return

def main():
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    load_ages()
    load_breeds()
    load_colors()
    load_images()
    return

if __name__ == '__main__':
    main()
    exit(0)
