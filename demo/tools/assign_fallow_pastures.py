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
    parser = ArgumentParser(description='Leave pastures fallow to recover nutrients')
    parser.add_argument('-p',
                        '--pasture',
                        type=str,
                        required=True,
                        help='pasture allocation')
    parser.add_argument('-u',
                        '--username',
                        type=str,
                        required=True,
                        choices=['foster',
                                 'berkeley'],
                        help='user')
    o = parser.parse_args()
    return(o.pasture, o.username)
    
def _get_data():
    return {'fallow': True}

def leave_fallow(pasture):
    from assets.models import Pasture
    from assets.serializers import PastureWriteSerializer

    try:
        instance = Pasture.objects.get(name=pasture)
        ps = PastureWriteSerializer(instance=instance,
                                    data=_get_data(),
                                    partial=True)
        if ps.is_valid() and len(ps.errors) == 0:
            ps.save()
            print('Pasture {} left fallow'.format(pasture))
            return
        else:
            print('ERROR: {}'.format(ps.errors))
            exit(1)
    except PermissionDenied as e:
        print('ERROR: {}'.format(e))
        print('ERROR: Unable to make pasture fallow!')
        exit(1)
    except IntegrityError as e:
        print('ERROR: {}'.format(e))
        exit(1)

def main():
    (pasture, username) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    from tools.utils import ToolData
    if ToolData.valid_pasture(pasture, username):
        leave_fallow(pasture)
    else:
        exit('ERROR: user: {} does not have access to {} pasture'.format(
            username, pasture))
    return

if __name__ == '__main__':
    main()
    exit(0)
