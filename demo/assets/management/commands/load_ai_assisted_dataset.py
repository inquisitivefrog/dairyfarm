import json
from datetime import date, datetime
from pathlib import Path
import random
from uuid import NAMESPACE_URL, uuid5

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from assets.models import Action, Age, Breed, CerealHay, Client, Color
from assets.models import Cow, Event, Exercise, GrassHay, HealthRecord
from assets.models import Illness, Injury, LegumeHay, Milk, Pasture, Season
from assets.models import Seed, Status
from summary.models import Annual, Monthly


DATASET_PATH = Path(settings.BASE_DIR) / (
    'demo/fixtures/ai_assisted_2019_2026/dataset.json')


class Command(BaseCommand):
    help = 'Load the separate Copilot-assisted 2019-2026 synthetic dataset.'

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            config = json.loads(DATASET_PATH.read_text())
        except (IOError, ValueError) as error:
            raise CommandError(
                'Could not read synthetic dataset {}: {}'.format(
                    DATASET_PATH, error))

        owner, created = User.objects.get_or_create(
            username=config['owner_username'],
            defaults={
                'first_name': 'AI Managed',
                'last_name': 'Farms',
                'email': 'ai-managed@example.invalid',
            },
        )
        if created:
            owner.set_unusable_password()
            owner.save(update_fields=['password'])
        references = config['reference_data']
        ages = [
            Age.objects.get_or_create(name=name)[0]
            for name in references['ages']
        ]
        if not ages:
            raise CommandError('Synthetic dataset must define cow ages.')
        breed = Breed.objects.get_or_create(
            name=references['breed']['name'],
            defaults={'url': references['breed']['url']},
        )[0]
        color = Color.objects.get_or_create(name=references['color'])[0]
        action = Action.objects.get_or_create(name=references['action'])[0]
        seasons = {
            season_name: Season.objects.get_or_create(
                name=season_name
            )[0]
            for season_name in config['seed_seasons']
        }
        cereal = CerealHay.objects.get_or_create(
            name=config['seed_types']['cereal'])[0]
        grass = GrassHay.objects.get_or_create(
            name=config['seed_types']['grass'])[0]
        legume = LegumeHay.objects.get_or_create(
            name=config['seed_types']['legume'])[0]
        statuses = {
            status_name: Status.objects.get_or_create(
                name=status_name
            )[0]
            for status_name in references['statuses']
        }
        illnesses = {
            item['diagnosis']: Illness.objects.get_or_create(
                diagnosis=item['diagnosis'],
                defaults={'treatment': item['treatment']},
            )[0]
            for item in references['illnesses']
        }
        injuries = {
            item['diagnosis']: Injury.objects.get_or_create(
                diagnosis=item['diagnosis'],
                defaults={'treatment': item['treatment']},
            )[0]
            for item in references['injuries']
        }
        healthy = statuses['Healthy']
        pregnant = statuses['Pregnant']
        injured = statuses['Injured']
        bacterial = statuses['Bacterial Illness']
        viral = statuses['Viral Illness']
        mastitis = illnesses['mastitis']
        respiratory_illness = illnesses['BRD']
        lameness = injuries['lameness']

        client, _ = Client.objects.get_or_create(
            name=config['client_name'],
            defaults={
                'user': owner,
                'join_date': datetime.strptime(
                    config['client_join_date'], '%Y-%m-%d').date(),
            },
        )
        if client.user_id != owner.pk:
            raise CommandError(
                'Synthetic client already exists under a different owner.')

        pastures = []
        for pasture_data in config['pastures']:
            pasture, _ = Pasture.objects.get_or_create(
                name=pasture_data['name'],
                defaults={
                    'client': client,
                    'url': pasture_data['url'],
                    'distance': pasture_data['distance'],
                },
            )
            if pasture.client_id != client.pk:
                raise CommandError(
                    'Pasture {} already belongs to another client.'.format(
                        pasture.name))
            pastures.append(pasture)

        cows = []
        for index in range(config['cow_count']):
            tag = uuid5(
                NAMESPACE_URL,
                '{}{}'.format(config['cow_rfid_namespace'], index + 1),
            )
            cow, _ = Cow.objects.get_or_create(
                rfid=tag,
                defaults={
                    'client': client,
                    'purchased_by': owner,
                    'purchase_date': date(config['years'][0], 1, 1),
                    'age': ages[index % len(ages)],
                    'breed': breed,
                    'color': color,
                },
            )
            if cow.client_id != client.pk:
                raise CommandError(
                    'RFID {} already belongs to another client.'.format(tag))
            cows.append(cow)

        cadence = config['records_per_cow_per_year']
        for year in config['years']:
            for cow_index, cow in enumerate(cows):
                pasture = pastures[cow_index % len(pastures)]
                for month in range(1, 13):
                    for milking_index in range(
                            cadence['milkings_per_month']):
                        day = 5 if milking_index == 0 else 20
                        when = self._datetime(year, month, day, 5)
                        variation_seed = (
                            year * 10000 + cow_index * 1000 +
                            month * 10 + milking_index)
                        variation = random.Random(
                            variation_seed).randint(-2, 2)
                        baseline = 4 + (cow_index % 5) + (month % 3)
                        gallons = max(1, int(round(
                            baseline *
                            (1 + config['milk_year_adjustments'][str(year)]) +
                            config['milk_month_adjustments'][month - 1] +
                            variation
                        )))
                        Milk.objects.update_or_create(
                            client=client,
                            cow=cow,
                            milking_time=when,
                            defaults={
                                'recorded_by': owner,
                                'gallons': gallons,
                            },
                        )

                    event_time = self._datetime(year, month, 10, 7)
                    Event.objects.get_or_create(
                        client=client,
                        cow=cow,
                        event_time=event_time,
                        action=action,
                        defaults={'recorded_by': owner},
                    )
                    Exercise.objects.get_or_create(
                        client=client,
                        cow=cow,
                        exercise_time=self._datetime(year, month, 15, 8),
                        pasture=pasture,
                        defaults={'recorded_by': owner},
                    )

                inspections = cadence['health_inspections_per_year']
                health_cases = config['annual_health_case_counts'][str(year)]
                for inspection_index in range(inspections):
                    month = 1 + inspection_index * 12 // inspections
                    year_offset = year - config['years'][0]
                    illness_record = None
                    injury_record = None
                    injury_case = (
                        inspection_index == 1 and
                        (cow_index * 3 + year_offset) % len(cows) <
                        health_cases['injuries'])
                    illness_case = (
                        inspection_index == 2 and
                        (cow_index + year_offset) % len(cows) <
                        health_cases['illnesses'])
                    if injury_case:
                        status = injured
                        injury_record = lameness
                    elif illness_case:
                        if (cow_index + year_offset) % 2:
                            status = viral
                            illness_record = respiratory_illness
                        else:
                            status = bacterial
                            illness_record = mastitis
                    else:
                        status = (
                            pregnant if cow_index % 4 == 0 and
                            inspection_index == 0 else healthy)
                    HealthRecord.objects.update_or_create(
                        client=client,
                        cow=cow,
                        inspection_time=self._datetime(
                            year, month, 12, 9),
                        defaults={
                            'recorded_by': owner,
                            'temperature': 101.0 + (cow_index % 4) * 0.2,
                            'respiratory_rate': 30 + cow_index,
                            'heart_rate': 55 + cow_index,
                            'blood_pressure': 135 + cow_index,
                            'weight': 450 + 10 * cow_index,
                            'body_condition_score': (
                                3.0 + (cow_index % 4) * 0.1),
                            'status': status,
                            'illness': illness_record,
                            'injury': injury_record,
                        },
                    )

            for pasture in pastures:
                for season_name in config['seed_seasons']:
                    Seed.objects.get_or_create(
                        client=client,
                        year=year,
                        season=seasons[season_name],
                        pasture=pasture,
                        defaults={
                            'seeded_by': owner,
                            'cereal_hay': cereal,
                            'grass_hay': grass,
                            'legume_hay': legume,
                        },
                    )

            annual, _ = Annual.objects.get_or_create(
                client=client,
                year=year,
                defaults={'created_by': owner},
            )
            annual.save()
            for month in range(1, 13):
                monthly, _ = Monthly.objects.get_or_create(
                    client=client,
                    year=year,
                    month=month,
                    defaults={'created_by': owner},
                )
                monthly.save()

        Cow.objects.filter(client=client).update(purchased_by=owner)
        Event.objects.filter(client=client).update(recorded_by=owner)
        Exercise.objects.filter(client=client).update(recorded_by=owner)
        HealthRecord.objects.filter(client=client).update(recorded_by=owner)
        Milk.objects.filter(client=client).update(recorded_by=owner)
        Seed.objects.filter(client=client).update(seeded_by=owner)
        Annual.objects.filter(client=client).update(created_by=owner)
        Monthly.objects.filter(client=client).update(created_by=owner)

        self.stdout.write(self.style.SUCCESS(
            'Loaded synthetic client "{}": {} cows, {} pastures, and data '
            'for {}-{}.'.format(
                client.name,
                len(cows),
                len(pastures),
                min(config['years']),
                max(config['years']),
            )))

    @staticmethod
    def _datetime(year, month, day, hour):
        return timezone.make_aware(datetime(year, month, day, hour))
