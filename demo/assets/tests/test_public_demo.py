from datetime import date, datetime

from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from assets.models import Age, Breed, Client, Color, Cow, HealthRecord, Milk
from assets.models import Status


@override_settings(
    PUBLIC_DEMO_READ_ONLY=True,
    PUBLIC_DEMO_CLIENT_NAME='Synthetic Public Farm',
)
class TestPublicDemo(APITestCase):
    def setUp(self):
        self.public_owner = User.objects.create_user(username='ai-managed')
        self.private_owner = User.objects.create_user(
            username='private-owner')
        self.public_client = Client.objects.create(
            user=self.public_owner,
            name='Synthetic Public Farm',
            join_date=date(2020, 1, 1),
        )
        self.private_client = Client.objects.create(
            user=self.private_owner,
            name='Private Farm',
            join_date=date(2020, 1, 1),
        )
        age = Age.objects.create(name='Adult')
        breed = Breed.objects.create(name='Synthetic Breed', url='/breed.png')
        color = Color.objects.create(name='Synthetic Color')
        self.private_cow = Cow.objects.create(
            client=self.private_client,
            purchased_by=self.private_owner,
            purchase_date=date(2020, 1, 1),
            age=age,
            breed=breed,
            color=color,
        )
        self.public_cow = Cow.objects.create(
            client=self.public_client,
            purchased_by=self.public_owner,
            purchase_date=date(2020, 1, 1),
            age=age,
            breed=breed,
            color=color,
        )
        private_record_time = timezone.make_aware(
            datetime(2020, 1, 15))
        HealthRecord.objects.create(
            client=self.private_client,
            recorded_by=self.private_owner,
            inspection_time=private_record_time,
            cow=self.private_cow,
            status=Status.objects.create(name='Bacterial Illness'),
        )
        Milk.objects.create(
            client=self.private_client,
            recorded_by=self.private_owner,
            milking_time=private_record_time,
            cow=self.private_cow,
            gallons=12,
        )
        Milk.objects.create(
            client=self.public_client,
            recorded_by=self.public_owner,
            milking_time=private_record_time,
            cow=self.public_cow,
            gallons=8,
        )

    def test_anonymous_client_and_cow_reads_only_return_public_farm(self):
        clients = self.client.get(reverse('assets:client-list'))
        cows = self.client.get(reverse('assets:cow-list'))

        self.assertEqual(status.HTTP_200_OK, clients.status_code)
        self.assertEqual(
            ['Synthetic Public Farm'],
            [item['name'] for item in clients.data['results']],
        )
        self.assertEqual(status.HTTP_200_OK, cows.status_code)
        self.assertEqual(
            [self.public_cow.pk],
            [item['id'] for item in cows.data['results']],
        )
        self.assertEqual([1], [
            item['farm_number'] for item in cows.data['results']])

        cow_detail = self.client.get(reverse(
            'assets:cow-detail',
            kwargs={'pk': self.public_cow.pk},
        ))
        self.assertEqual(1, cow_detail.data['farm_number'])

    def test_public_milk_sequence_starts_at_one_after_other_farm_records(self):
        milk = self.client.get(reverse(
            'assets:milk-list-client',
            kwargs={'pk': self.public_client.pk},
        ))

        self.assertEqual(status.HTTP_200_OK, milk.status_code)
        self.assertEqual([1], [
            item['farm_number'] for item in milk.data['results']])

    def test_anonymous_cannot_read_private_farm_by_id(self):
        response = self.client.get(reverse(
            'assets:cow-detail',
            kwargs={'pk': self.private_cow.pk},
        ))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_summary_endpoints_exclude_private_farm_records(self):
        milk = self.client.get(reverse(
            'assets:milk-summary-month',
            kwargs={'year': '2020', 'month': '01'},
        ))
        illness = self.client.get(reverse(
            'assets:healthrecord-illness-summary-month',
            kwargs={'year': '2020', 'month': '01'},
        ))

        self.assertEqual(status.HTTP_200_OK, milk.status_code)
        self.assertEqual(8, milk.data[0]['gallons'])
        self.assertEqual(status.HTTP_200_OK, illness.status_code)
        self.assertEqual(0, illness.data[0]['status'])

    def test_public_profile_list_does_not_disclose_accounts(self):
        response = self.client.get(reverse('assets:user-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data['results'])

    def test_public_home_page_bootstraps_read_only_synthetic_profile(self):
        response = self.client.get('/')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertContains(response, 'data-public-demo="true"')
        self.assertContains(response, 'data-public-demo-client-id="{}"'.format(
            self.public_client.pk))

    def test_public_mode_rejects_api_writes_even_for_authenticated_users(self):
        anonymous_response = self.client.post(
            reverse('assets:cow-list'),
            {},
        )
        self.client.force_authenticate(user=self.public_owner)

        authenticated_response = self.client.post(
            reverse('assets:cow-list'),
            {},
        )

        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED,
            anonymous_response.status_code,
        )
        self.assertEqual(
            status.HTTP_403_FORBIDDEN,
            authenticated_response.status_code,
        )

    def test_public_mode_denies_legacy_account_login_and_profile_endpoints(
            self):
        login_response = self.client.post(
            reverse('login'),
            {'username': 'private-owner', 'password': 'anything'},
        )
        self.client.force_login(self.private_owner)
        profile_response = self.client.get(reverse('ui_logged_in'))

        self.assertEqual(
            status.HTTP_403_FORBIDDEN,
            login_response.status_code,
        )
        self.assertEqual(
            status.HTTP_403_FORBIDDEN,
            profile_response.status_code,
        )


@override_settings(PUBLIC_DEMO_READ_ONLY=False)
class TestPublicDemoDisabled(APITestCase):
    def test_anonymous_api_access_remains_disabled_by_default(self):
        response = self.client.get(reverse('assets:client-list'))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
