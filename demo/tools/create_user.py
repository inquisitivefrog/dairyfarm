#!/usr/bin/env python3

from argparse import ArgumentParser
from getpass import getpass
import os
import sys

from django import setup
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


def read_args():
    parser = ArgumentParser(description='Create a Django user account')
    parser.add_argument('-f', '--firstname', default=None,
                        help='first name of user')
    parser.add_argument('-l', '--lastname', default=None,
                        help='last name of user')
    parser.add_argument('-e', '--email', required=True,
                        help='email address of user')
    parser.add_argument('-u', '--username', required=True,
                        help='username of user')
    parser.add_argument('--staff', action='store_true',
                        help='grant Django admin-site staff access')
    parser.add_argument('-s', '--superuser', action='store_true',
                        help='grant all Django permissions')
    return parser.parse_args()


def create_user(first_name, last_name, email, username, password,
                staff=False, superuser=False):
    from django.contrib.auth.models import User

    if User.objects.filter(username=username).exists():
        raise ValueError('username already exists')
    if len(password) < 12:
        raise ValueError('password must be at least 12 characters')

    user_data = {
        'username': username,
        'email': email,
        'first_name': first_name or '',
        'last_name': last_name or '',
    }
    try:
        validate_password(password, user=User(**user_data))
    except ValidationError as error:
        raise ValueError('; '.join(error.messages))
    try:
        if superuser:
            user = User.objects.create_superuser(
                password=password,
                **user_data
            )
        else:
            user = User.objects.create_user(
                password=password,
                **user_data
            )
            if staff:
                user.is_staff = True
                user.save(update_fields=['is_staff'])
    except IntegrityError:
        raise ValueError(
            'account could not be created; check username and email')
    return user


def main():
    args = read_args()
    password = getpass('Password: ')
    confirmation = getpass('Confirm password: ')
    if not password:
        print('ERROR: password must not be empty', file=sys.stderr)
        return 1
    if password != confirmation:
        print('ERROR: passwords do not match', file=sys.stderr)
        return 1

    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
    setup()

    try:
        user = create_user(
            args.firstname,
            args.lastname,
            args.email,
            args.username,
            password,
            staff=args.staff,
            superuser=args.superuser,
        )
    except ValueError as error:
        print('ERROR: {}'.format(error), file=sys.stderr)
        return 1
    print('Created {} account: {}'.format(
        'superuser' if user.is_superuser else (
            'staff' if user.is_staff else 'regular'),
        user.username,
    ))
    return 0


if __name__ == '__main__':
    sys.exit(main())
