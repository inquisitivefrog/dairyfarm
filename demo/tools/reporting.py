#!/Users/tim/demo/bin/python3

from argparse import ArgumentParser
from os import environ
from random import randint
from sys import exit, path

from django import setup
from django.conf import settings

def read_args():
    parser = ArgumentParser(description='report recent activity')
    parser.add_argument('-t',
                        '--duration',
                        type=str,
                        choices=['annual', 'monthly'],
                        required=False,
                        default='annual',
                        help='annual or monthly')
    parser.add_argument('-u',
                        '--username',
                        required=False,
                        type=str,
                        choices=['farmer', 'farmhand', 'vet'],
                        default='',
                        help='existing user by username')
    parser.add_argument('-y',
                        '--year',
                        required=False,
                        type=str,
                        choices=['2015', '2016', '2017', '2018'],
                        default=None,
                        help='year in %Y format')
    parser.add_argument('-m',
                        '--month',
                        required=False,
                        type=str,
                        choices=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
                        default=None,
                        help='month in %m format')
    o = parser.parse_args()
    return (o.duration,
            o.username,
            o.year,
            o.month)

def generate_annual_report(data):
    from summary.models import Annual
    a = Annual.objects.create(**data)
    return

def display_annual_report(year):
    from django.db.models import Max
    from summary.models import Annual
    a = Annual.objects.filter(year=year).aggregate(Max('id'))
    return

def generate_monthly_report(data):
    from summary.models import Monthly
    m = Monthly.objects.create(**data)
    return

def display_monthly_report(year, month):
    from django.db.models import Max
    from summary.models import Monthly
    m = Monthly.objects.filter(year=year,
                               month=month).aggregate(Max('id'))
    return

def main():
    (duration, username, year, month) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    from django.contrib.auth.models import User
    user = User.objects.get(username=username)
    data = {'created_by': user,
            'year': year} 
    if duration == 'annual':
        generate_annual_report(data)
        print(display_annual_report(year))
    elif duration == 'monthly':
        data.update({'month': month}) 
        generate_monthly_report(data)
        print(display_monthly_report(year,
                                     month))
    return

if __name__ == '__main__':
    main()
    exit(0)
