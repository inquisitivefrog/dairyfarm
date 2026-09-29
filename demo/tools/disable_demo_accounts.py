#!/usr/bin/env python3
"""Disable accounts whose demo credentials were exposed in repository history.

Dry-run by default:
    python tools/disable_demo_accounts.py

Apply to the configured Django database:
    python tools/disable_demo_accounts.py --apply
"""

from argparse import ArgumentParser
import json
import os
import sys

from django import setup
from django.db import transaction


def fixture_usernames():
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fixture_path = os.path.join(
        project_path, 'demo', 'fixtures', 'user.json')
    with open(fixture_path, encoding='utf-8') as fixture:
        records = json.load(fixture)
    return [
        record['fields']['username']
        for record in records
        if record.get('model') == 'auth.user'
    ]


def disable_accounts(usernames, apply=False):
    from django.contrib.auth.models import User

    users = list(User.objects.filter(username__in=usernames))
    if apply:
        with transaction.atomic():
            for user in users:
                user.set_unusable_password()
                user.is_active = False
                user.is_staff = False
                user.is_superuser = False
                user.save(update_fields=[
                    'password',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ])
    return users


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        '--apply',
        action='store_true',
        help=(
            'disable accounts in the configured database '
            '(dry-run by default)'
        ),
    )
    args = parser.parse_args()

    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
    setup()

    users = disable_accounts(fixture_usernames(), apply=args.apply)
    action = 'Disabled' if args.apply else 'Would disable'
    print('{} {} demo account(s).{}'.format(
        action,
        len(users),
        '' if args.apply else ' Re-run with --apply to make this change.',
    ))
    return 0


if __name__ == '__main__':
    sys.exit(main())
