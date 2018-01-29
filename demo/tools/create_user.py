#!/Users/tim/demo/bin/python3

from argparse import ArgumentParser
from os import environ
from sys import exit, path

from django import setup
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.utils import IntegrityError

def read_args():
    parser = ArgumentParser(description='Create User for Authentication')
    parser.add_argument('-f',
                        '--firstname',
                        type=str,
                        required=False,
                        default=None,
                        help='first name of user')
    parser.add_argument('-l',
                        '--lastname',
                        type=str,
                        required=False,
                        default=None,
                        help='last name of user')
    parser.add_argument('-e',
                        '--email',
                        type=str,
                        required=True,
                        help='email address of user')
    parser.add_argument('-u',
                        '--username',
                        type=str,
                        required=True,
                        help='username of user')
    parser.add_argument('-p',
                        '--password',
                        type=str,
                        required=True,
                        help='password for security')
    o = parser.parse_args()
    return(o.firstname,
           o.lastname,
           o.email,
           o.username,
           o.password)
    
def create_user(first_name, last_name, email, username, password):
    data = {'email': email,
            'username': username}
    if first_name:
        data.update({'first_name': first_name})
    if last_name:
        data.update({'last_name': last_name})
    from django.contrib.auth.models import User
    try:
        user = User(**data)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.save()
        return
    except PermissionDenied as e:
        print('ERROR: unable to create username: {}!'.format(username))
        exit(1)
    except IntegrityError as e:
        print('ERROR: username: {} already exists!'.format(username))
        exit(1)

def main():
    (firstname, lastname, email, username, password) = read_args()
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'demo.settings')
    setup()
    create_user(firstname, lastname, email, username, password)
    return

if __name__ == '__main__':
    main()
    exit(0)
