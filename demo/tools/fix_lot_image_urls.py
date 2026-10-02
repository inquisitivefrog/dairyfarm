#!/usr/bin/env python3
"""Align Lot_1–Lot_9 pasture URLs with their case-sensitive image filenames.

Run from the demo directory:
    python tools/fix_lot_image_urls.py
"""

import os
import sys

from django import setup
from django.conf import settings
from django.db import transaction


def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
    setup()

    from assets.models import Pasture

    updates = []
    for number in range(1, 10):
        name = 'Lot_{}'.format(number)
        relative_url = '/static/images/regions/{}.png'.format(name)
        image_path = os.path.join(
            settings.BASE_DIR,
            'static/images/regions/{}.png'.format(name),
        )
        if not os.path.isfile(image_path):
            raise RuntimeError(
                'Expected pasture image is missing: {}'.format(image_path))
        updates.append((name, relative_url))

    changed = 0
    with transaction.atomic():
        for name, relative_url in updates:
            changed += Pasture.objects.filter(
                name=name,
            ).exclude(
                url=relative_url,
            ).update(url=relative_url)

    print('Verified {} pasture image files; updated {} database URLs.'.format(
        len(updates), changed))
    for name, relative_url in updates:
        count = Pasture.objects.filter(name=name, url=relative_url).count()
        print('{}: {} ({})'.format(name, relative_url, count))


if __name__ == '__main__':
    main()
