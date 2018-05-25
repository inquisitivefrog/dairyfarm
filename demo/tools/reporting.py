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
                        choices=['farmer', 'farmhand', 'vet', 'foster', 'berkeley'],
                        default='',
                        help='existing user by username')
    parser.add_argument('-y',
                        '--year',
                        required=False,
                        type=int,
                        choices=[2015, 2016, 2017, 2018],
                        default=None,
                        help='year in %Y format')
    parser.add_argument('-m',
                        '--month',
                        required=False,
                        type=int,
                        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        default=None,
                        help='month in %m format')
    o = parser.parse_args()
    return (o.duration,
            o.username,
            o.year,
            o.month)

def generate_annual_report(data):
    from summary.serializers import AnnualWriteSerializer
    aws = AnnualWriteSerializer(data=data)
    if aws.is_valid():
        aws.save()
        return
    else:
        exit('ERROR: AnnualWriteSerializer failed: '.format(aws.errors))

def display_annual_report(client, year):
    from summary.models import Annual
    print([ a.id for a in Annual.objects.filter(client=client, year=year)])
    return

def generate_monthly_report(data):
    from summary.serializers import MonthlyWriteSerializer

    mws = MonthlyWriteSerializer(data=data)
    if mws.is_valid():
        mws.save()
        return
    else:
        exit('ERROR: MonthlyWriteSerializer failed: '.format(mws.errors))

def display_monthly_report(client, year, month):
    from summary.models import Monthly
    print([ m.id for m in Monthly.objects.filter(client=client, year=year, month=month)])
    return

def main():
    (duration, username, year, month) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    from django.contrib.auth.models import User
    from assets.models import Client
    user = User.objects.get(username=username)
    client = Client.objects.get(user=user)
    data = {'created_by': username,
            'client': client.name,
            'year': year} 
    if duration == 'annual':
        generate_annual_report(data)
        display_annual_report(client.id, year)
    elif duration == 'monthly':
        data.update({'month': month}) 
        generate_monthly_report(data)
        display_monthly_report(client.id, year, month)
    return

if __name__ == '__main__':
    main()
    exit(0)
