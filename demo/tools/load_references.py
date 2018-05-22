#!/Users/tim/demo/bin/python3

from os import environ
from random import randint
from sys import exit, path

from django import setup
from django.conf import settings

def load_actions():
    from assets.models import Action
    actions = ['Call Vet',
               'Chew cud',
               'Drink',
               'Exercise in pen',
               'Get diagnosed',
               'Get inspected',
               'Get treated',
               'Get milked',
               'Graze',
               'Nap',
               'Pedicure',
               'Rest in pen',
               'Return to barn',
               'Sleep',
               'Visit vet',
               'Walk to pasture',
               'Wake Up']
    for action in actions:
        data = {'name': action}
        Action.objects.create(**data)
        print('Defined action: {}'.format(action))
    return

def load_ages():
    from assets.models import Age
    ages = ['1 year', '2 years', '3 years', '4 years', '5 years']
    for age in ages:
        data = {'name': age}
        Age.objects.create(**data)
        print('Defined age: {}'.format(age))
    return

def load_clients():
    from django.contrib.auth.models import User
    from assets.models import Client
    from tools.utils import ToolTime
    clients = ['Foster Farms Dairy',
               'Berkeley Farms',
               'McClelland Dairy',
               'Clauss Dairy Farms',
               'Dairy Farmers of America']
    for client in clients:
        username = client.split()[0].lower()
        user = User.objects.get(username=username)        
        data = {'name': client,
                'join_date': ToolTime.get_date(),
                'user': user}
        Client.objects.create(**data)
    return

def load_colors():
    from assets.models import Breed, Color
    colors = ['black_white', 'red_white', 'brown', 'tawny', 'golden_white',
              'gray', 'red', 'white', 'roan']
    for color in colors:
        data = {'name': color}
        Color.objects.create(**data)
    return

def load_breeds():
    from assets.models import Breed, Color
    breeds = {'Holstein': ['black_white', 'red_white'],
              'Jersey': ['brown', 'tawny'],
              'Guernsey': ['golden_white'],
              'Ayrshire': ['golden_white'],
              'Brown Swiss': ['brown', 'gray'],
              'Milking Shorthorn': ['red', 'white', 'roan', 'red_white'],
              'Dutch Belted': ['black_white']}
    images = {'Holstein': '/static/images/breeds/holstein.png',
              'Jersey': '/static/images/breeds/jersey.png',
              'Guernsey': '/static/images/breeds/guernsey.png',
              'Ayrshire': '/static/images/breeds/ayrshire.png',
              'Brown Swiss': '/static/images/breeds/brown_swiss.png',
              'Milking Shorthorn': '/static/images/breeds/milking_shorthorn.png',
              'Dutch Belted': '/static/images/breeds/dutch_belted.png'}
    for breed in breeds: 
        data = {'name': breed,
                'url': images[breed]}
        Breed.objects.create(**data)
        print('Defined breed: {}'.format(breed))
    return

def load_cereal_hay():
    from assets.models import CerealHay
    cereals = ['alfalfa', 'barley', 'oat', 'rye', 'wheat']
    for cereal in cereals:
        data = {'name': cereal}
        CerealHay.objects.create(**data)
        print('Defined cereal hay: {}'.format(cereal))
    return

def load_grass_hay():
    from assets.models import GrassHay
    hay = ['bermuda', 'bluegrass', 'brome', 'fescue', 'orchardgrass',
           'reed canary grass', 'ryegrass', 'sudangrass', 'timothy']
    for grass in hay:
        data = {'name': grass}
        GrassHay.objects.create(**data)
        print('Defined grass hay: {}'.format(grass))
    return

def load_legume_hay():
    from assets.models import LegumeHay
    legumes = ['clover', 'cowpeas', 'lespedeza', 'soybean',
               'trefoil', 'vetch']
    for legume in legumes:
        data = {'name': legume}
        LegumeHay.objects.create(**data)
        print('Defined legume hay: {}'.format(legume))
    return

def load_injuries():
    from assets.models import Injury
    meds = {'chapped teat': 'apply salve',
            'lameness': 'pedicure',
            'sprain': 'bandage leg, avoid walking',
            'swollen knee': 'get innoculated, avoid walking',
            'sore lower back': 'temporarily avoid breeding'}
    for diagnosis, treatment in meds.items():
        data = {'diagnosis': diagnosis,
                'treatment': treatment}
        Injury.objects.create(**data)
        print('Defined treatment: {} for diagnosis: {}'.format(treatment, diagnosis))
    return

def load_illnesses():
    from assets.models import Illness
    meds = {'fever': 'feed aspirin',
            'infection': 'get diagnosed',
            'TRP': 'feed magnet, monitor with ultrasound, wait it out',
            'BRD': 'feed antimicrobials',
            'MAP': 'feed antimicrobials',
            'RP': 'trim excess tissue, wait it out',
            'endometritis': 'feed antimicrobials',
            'mastitis': 'feed antimicrobials',
            'metritis': 'feed antimicrobials',
            'ketosis': 'injest bolus glucose',
            'milk fever': 'teat dipping',
            'pseudocowpox': 'teat dipping',
            'digital dermatitis': 'apply antibiotic powder',
            'copper toxicity': 'change feed',
            'acidosis': 'change feed'}
    for diagnosis, treatment in meds.items():
        data = {'diagnosis': diagnosis,
                'treatment': treatment}
        Illness.objects.create(**data)
        print('Defined treatment: {} for diagnosis: {}'.format(treatment, diagnosis))
    return

def load_pastures():
    from django.contrib.auth.models import User
    from assets.models import Client, Pasture
    user = User.objects.get(username='foster')
    client = Client.objects.get(user=user)
    ff_pastures = {'North': '/static/images/regions/north.jpg',
                   'West': '/static/images/regions/west.jpg',
                   'South': '/static/images/regions/south.jpg',
                   'East': '/static/images/regions/east.jpg',
                   'Central North': '/static/images/regions/central_north.jpg',
                   'Central West': '/static/images/regions/central_west.jpg',
                   'Central South': '/static/images/regions/central_south.jpg',
                   'Central East': '/static/images/regions/central_east.jpg',
                   'North West': '/static/images/regions/north_west.jpg',
                   'North East': '/static/images/regions/north_east.jpg',
                   'South West': '/static/images/regions/south_west.jpg',
                   'South East': '/static/images/regions/south_east.jpg',
                   'Pen': '/static/images/regions/pen.png'}
    for name, url in ff_pastures.items(): 
        data = {'client': client,
                'name': name,
                'url': url,
                'fallow': False,
                'distance': randint(1, 10)}
        if name not in ['South West', 'South East', 'Pen']:
            Pasture.objects.create(**data)
        else:
            data.update({'fallow': True})
            Pasture.objects.create(**data)
        print('Defined pasture: {}'.format(name))
    user = User.objects.get(username='berkeley')
    client = Client.objects.get(user=user)
    b_pastures = {'Lot_1': '/static/images/regions/lot_1.png',
                  'Lot_2': '/static/images/regions/lot_2.png',
                  'Lot_3': '/static/images/regions/lot_3.png',
                  'Lot_4': '/static/images/regions/lot_4.png',
                  'Lot_5': '/static/images/regions/lot_5.png',
                  'Lot_6': '/static/images/regions/lot_6.png',
                  'Lot_7': '/static/images/regions/lot_7.png',
                  'Lot_8': '/static/images/regions/lot_8.png',
                  'Lot_9': '/static/images/regions/lot_9.png'}
    for name, url in b_pastures.items(): 
        data = {'client': client,
                'name': name,
                'url': url,
                'fallow': False,
                'distance': randint(1, 10)}
        if name not in ['Lot_9']:
            Pasture.objects.create(**data)
        else:
            data.update({'fallow': True})
            Pasture.objects.create(**data)
        print('Defined pasture: {}'.format(name))
    return

def load_seasons():
    from assets.models import Season
    names = ['Spring',
             'Summer',
             'Autumn',
             'Winter']
    for name in names:
        data = {'name': name}
        Season.objects.create(**data)
        print('Defined season: {}'.format(name))
    return

def load_statuses():
    from assets.models import Status
    conditions = ['Healthy',
                  'Pregnant',
                  'Injured',
                  'Viral Illness',
                  'Bacterial Illness']
    for status in conditions:
        data = {'name': status}
        Status.objects.create(**data)
        print('Defined status: {}'.format(status))
    return

def load_treatments():
    from assets.models import Treatment
    treatments = ['apply salve', 'apply antibiotic powder',
                  'bandage leg, avoid walking', 'change feed',
                  'feed antimicrobials', 'feed aspirin',
                  'feed magnet, monitor with ultrasound, wait it out',
                  'get diagnosed', 'get innoculated, avoid walking',
                  'injest bolus glucose', 'pedicure', 'teat dipping',
                  'temporarily avoid breeding',
                  'trim excess tissue, wait it out']
    for treatment in treatments:
        data = {'name': treatment}
        Treatment.objects.create(**data)
        print('Defined treatment: {}'.format(treatment))
    return

def load_vaccines():
    from assets.models import Vaccine
    vaccines = ['BRD vaccine', 'MAP vaccine',
                'endometritis vaccine', 'mastitis vaccine',
                'metritis vaccine', 'ketosis vaccine']
    for vaccine in vaccines:
        data = {'name': vaccine}
        Vaccine.objects.create(**data)
        print('Defined vaccine: {}'.format(vaccine))
    return

def main():
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    load_actions()
    load_ages()
    load_clients()
    load_colors()
    load_breeds()
    load_cereal_hay()
    load_grass_hay()
    load_legume_hay()
    load_injuries()
    load_illnesses()
    load_pastures()
    load_seasons()
    load_statuses()
    load_treatments()
    load_vaccines()
    return

if __name__ == '__main__':
    main()
    exit(0)
