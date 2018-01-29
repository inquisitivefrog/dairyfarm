#!/Users/tim/demo/bin/python3

from os import environ
from sys import exit, path

from django import setup
from django.conf import settings
from django.core.management import execute_from_command_line

def get_db_tables():
    db_tables = {'user.json': 'auth.user',
                 'group.json': 'auth.group',
                 'permission.json': 'auth.permission',
                 'group_permission.json': 'auth.group_permissions',
                 'user_groups.json': 'auth.user_groups',
                 'user_permission.json': 'auth.user_user_permissions',
                 'age.json': 'assets.age',
                 'breed.json': 'assets.breed',
                 'color.json': 'assets.color',
                 'cow.json': 'assets.cow',
                 'image.json': 'assets.image'}
    return db_tables

def main():
    path.append('/Users/tim/Documents/workspace/python3/dairyfarm/demo/')
    environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
    setup()
    for key, value in get_db_tables().items():
        print('key: {}'.format(key))
        print('value: {}'.format(value))
        execute_from_command_line(['manage.py',
                                   'dumpdata',
                                   '--indent',
                                   '4',
                                   '--output',
                                   '{}/{}'.format(settings.FIXTURE_DIRS[0], key),
                                   value])
    return

if __name__ == '__main__':
    main()
    exit(0)
