from datetime import date
from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from assets.models import Client, Cow, Event, Exercise, HealthRecord
from assets.models import Milk, Pasture, Seed
from summary.models import Annual, Monthly


class TestAIassistedDataset(TestCase):
    def test_does_not_take_over_existing_farm_owned_by_other_user(self):
        existing_owner = User.objects.create_user(username='legacy-owner')
        existing_client = Client.objects.create(
            user=existing_owner,
            name='AI-Assisted Demo Farm (2019-2026)',
            join_date=date(2019, 1, 1),
        )

        with self.assertRaises(CommandError):
            call_command('load_ai_assisted_dataset', stdout=StringIO())

        existing_client.refresh_from_db()
        self.assertEqual(existing_owner, existing_client.user)
        self.assertFalse(User.objects.filter(username='ai-managed').exists())
        self.assertFalse(Cow.objects.exists())

    def test_loads_isolated_dataset_idempotently_and_generates_reports(self):
        call_command(
            'load_ai_assisted_dataset',
            stdout=StringIO(),
        )
        client = Client.objects.get(
            name='AI-Assisted Demo Farm (2019-2026)')
        ai_owner = User.objects.get(username='ai-managed')

        self.assertEqual(ai_owner, client.user)
        self.assertFalse(ai_owner.has_usable_password())
        self.assertEqual(
            ['ai-managed'],
            list(User.objects.values_list('username', flat=True)),
        )
        self.assertEqual(1, Client.objects.count())
        self.assertEqual(8, Cow.objects.filter(client=client).count())
        self.assertEqual(4, Pasture.objects.filter(client=client).count())
        self.assertEqual(1536, Milk.objects.filter(client=client).count())
        self.assertEqual(768, Event.objects.filter(client=client).count())
        self.assertEqual(768, Exercise.objects.filter(client=client).count())
        self.assertEqual(
            256, HealthRecord.objects.filter(client=client).count())
        self.assertEqual(128, Seed.objects.filter(client=client).count())
        self.assertEqual(8, Annual.objects.filter(client=client).count())
        self.assertEqual(96, Monthly.objects.filter(client=client).count())

        annual_2026 = Annual.objects.get(client=client, year=2026)
        monthly_2026 = Monthly.objects.get(
            client=client,
            year=2026,
            month=12,
        )
        self.assertLessEqual(len(annual_2026.link), 100)
        self.assertLessEqual(len(monthly_2026.link), 100)
        self.assertEqual(8, annual_2026.total_cows)
        self.assertGreater(annual_2026.gallons_milk, 0)
        self.assertGreater(monthly_2026.gallons_milk, 0)
        annual_reports = list(
            Annual.objects.filter(client=client).order_by('year'))
        milk_totals = [report.gallons_milk for report in annual_reports]
        self.assertGreater(len(set(milk_totals)), 1)
        self.assertTrue(all(report.ill_cows > 0 for report in annual_reports))
        self.assertTrue(all(
            report.injured_cows > 0 for report in annual_reports))
        self.assertGreater(
            len(set(report.ill_cows for report in annual_reports)),
            1,
        )
        self.assertGreater(
            len(set(report.injured_cows for report in annual_reports)),
            1,
        )
        self.assertTrue(
            HealthRecord.objects.filter(
                client=client,
                status__name='Bacterial Illness',
                illness__isnull=False,
            ).exists())
        self.assertTrue(
            HealthRecord.objects.filter(
                client=client,
                status__name='Injured',
                injury__isnull=False,
            ).exists())
        self.assertEqual(
            {ai_owner.pk},
            set(Cow.objects.filter(client=client).values_list(
                'purchased_by_id', flat=True)),
        )
        self.assertEqual(
            {ai_owner.pk},
            set(Milk.objects.filter(client=client).values_list(
                'recorded_by_id', flat=True)),
        )
        self.assertEqual(
            2019,
            Cow.objects.filter(client=client).earliest(
                'purchase_date').purchase_date.year,
        )
        self.client.force_login(ai_owner)
        logged_in = self.client.get(reverse('ui_logged_in')).json()
        self.assertEqual(
            [client.name],
            [item['name'] for item in logged_in['user']['clients']],
        )
        annual_response = self.client.get(reverse(
            'summary:annual-client-year',
            kwargs={'pk': client.pk, 'year': 2026},
        ))
        self.assertEqual(200, annual_response.status_code)
        self.assertEqual(2026, annual_response.json()[0]['year'])
        annual_2019 = Annual.objects.get(client=client, year=2019)
        monthly_2019_january = Monthly.objects.get(
            client=client,
            year=2019,
            month=1,
        )
        self.assertEqual(
            reverse(
                'summary:monthly-client-year',
                kwargs={'pk': client.pk, 'year': 2019},
            ),
            annual_2019.link,
        )
        self.assertEqual(
            reverse(
                'summary:monthly-client-year-month',
                kwargs={'pk': client.pk, 'year': 2019, 'month': '01'},
            ),
            monthly_2019_january.link,
        )
        monthly_response = self.client.get(annual_2019.link)
        self.assertEqual(200, monthly_response.status_code)
        self.assertEqual(12, len(monthly_response.json()))
        self.assertEqual(
            [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November',
                'December',
            ],
            [row['month'] for row in monthly_response.json()],
        )

        call_command(
            'load_ai_assisted_dataset',
            stdout=StringIO(),
        )
        self.assertEqual(1, Client.objects.count())
        self.assertEqual(1536, Milk.objects.filter(client=client).count())
        self.assertEqual(96, Monthly.objects.filter(client=client).count())
        self.assertEqual(ai_owner, Client.objects.get(pk=client.pk).user)
        self.assertGreater(
            Annual.objects.filter(client=client).values_list(
                'gallons_milk', flat=True).distinct().count(),
            1,
        )
        self.assertEqual(1, User.objects.count())
