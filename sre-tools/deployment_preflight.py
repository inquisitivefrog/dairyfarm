#!/usr/bin/env python3
"""Fail closed when application deployment settings are not production-ready.

Run from the repository root in the deployment image:
    python sre-tools/deployment_preflight.py

This gate checks the runtime baseline, required environment configuration, and
Django's deployment system checks. It does not replace an infrastructure or
application security review.
"""

import os
import sys


MINIMUM_PYTHON = (3, 10)
MINIMUM_DJANGO = (5, 2)
MINIMUM_HSTS_SECONDS = 31536000


def main():
    repository_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    project_path = os.path.join(repository_root, 'demo')
    sys.path.insert(0, project_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

    blockers = []
    if sys.version_info[:2] < MINIMUM_PYTHON:
        blockers.append(
            'Python {}.{} is below the supported deployment baseline 3.10'
            .format(sys.version_info[0], sys.version_info[1]))

    try:
        import django
        from django import setup
        from django.conf import settings
        from django.core.checks import run_checks
        from django.core.exceptions import ImproperlyConfigured
    except ImportError as error:
        print(
            'BLOCKED: cannot load Django deployment checks: {}'.format(error),
            file=sys.stderr,
        )
        return 1

    django_version = tuple(django.VERSION[:2])
    if django_version < MINIMUM_DJANGO:
        blockers.append(
            'Django {}.{} is below the supported deployment baseline 5.2'
            .format(django_version[0], django_version[1]))

    try:
        setup()
    except ImproperlyConfigured as error:
        print(
            'BLOCKED: Django settings could not initialize: {}'.format(error),
            file=sys.stderr,
        )
        return 1

    if os.environ.get('DJANGO_ENVIRONMENT', '').lower() != 'production':
        blockers.append(
            'DJANGO_ENVIRONMENT must be explicitly set to production')
    if settings.DEBUG:
        blockers.append('DJANGO_DEBUG must be false')
    if not settings.ALLOWED_HOSTS or '*' in settings.ALLOWED_HOSTS:
        blockers.append('DJANGO_ALLOWED_HOSTS must list explicit hostnames')
    if len(settings.SECRET_KEY) < 50 or 'replace-with-' in settings.SECRET_KEY:
        blockers.append(
            'DJANGO_SECRET_KEY must be a generated secret of at least 50 '
            'characters')
    if 'sqlite' in settings.DATABASES['default']['ENGINE'].lower():
        blockers.append('deployment database must not use SQLite')
    if not getattr(settings, 'SECURE_SSL_REDIRECT', False):
        blockers.append('SECURE_SSL_REDIRECT must be enabled')
    if not getattr(settings, 'SESSION_COOKIE_SECURE', False):
        blockers.append('SESSION_COOKIE_SECURE must be enabled')
    if not getattr(settings, 'CSRF_COOKIE_SECURE', False):
        blockers.append('CSRF_COOKIE_SECURE must be enabled')
    if getattr(settings, 'SECURE_HSTS_SECONDS', 0) < MINIMUM_HSTS_SECONDS:
        blockers.append(
            'SECURE_HSTS_SECONDS must be at least {}'.format(
                MINIMUM_HSTS_SECONDS))

    try:
        check_messages = run_checks(include_deployment_checks=True)
    except TypeError:
        blockers.append(
            'Django deployment checks are unavailable; upgrade Django first')
        check_messages = []

    for message in check_messages:
        if message.level >= 20:
            blockers.append(
                'Django check {}: {}'.format(message.id, message.msg))

    if blockers:
        print(
            'BLOCKED: deployment preflight found {} issue(s):'.format(
                len(blockers)),
            file=sys.stderr,
        )
        for blocker in blockers:
            print('- {}'.format(blocker), file=sys.stderr)
        return 1

    print('PASS: production deployment configuration checks are clear')
    return 0


if __name__ == '__main__':
    sys.exit(main())
