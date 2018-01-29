
from random import randint

def get_random_age():
    age = randint(5, 10)
    return '{} years'.format(age)

def get_random_breed():
    breeds = ['Criollo', 'Pineywood', 'Randall', 'Belgian Blue',
              'American Milking Devon', 'Guzerat', 'Red Sindhi']
    breed = randint(0, len(breeds) - 1)
    return breeds[breed]

def get_random_color():
    colors = ['Blue', 'Green', 'Orange', 'Yellow']
    color = randint(0, len(colors) - 1)
    return colors[color]

def get_random_image():
    images = ['/static/images/criollo.png',
              '/static/images/pineywood.png',
              '/static/images/randall.png',
              '/static/images/belgian_blue.png',
              '/static/images/american_milking_devon.png',
              '/static/images/guzerat.png',
              '/static/images/red_sindhi.png']
    image = randint(0, len(images) - 1)
    return images[image]
