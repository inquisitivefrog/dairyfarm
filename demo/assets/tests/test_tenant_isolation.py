from datetime import date, datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from assets.models import Action, Age, Breed, Client, Color, Cow, Event
from assets.models import HealthRecord, Milk, Pasture, Status
from summary.models import Annual


class TestTenantIsolation(APITestCase):
    def setUp(self):
        self.owner_a = User.objects.create_user(
            username='owner-a',
            password='owner-a-password',
        )
        self.owner_b = User.objects.create_user(
            username='owner-b',
            password='owner-b-password',
        )
        self.client_a = Client.objects.create(
            user=self.owner_a,
            name='Synthetic Farm A',
            join_date=date(2020, 1, 1),
        )
        self.client_b = Client.objects.create(
            user=self.owner_b,
            name='Synthetic Farm B',
            join_date=date(2020, 1, 1),
        )
        age = Age.objects.create(name='Adult')
        breed = Breed.objects.create(
            name='Synthetic Breed',
            url='https://example.test',
        )
        color = Color.objects.create(name='Synthetic Color')
        self.cow_a = Cow.objects.create(
            client=self.client_a,
            purchased_by=self.owner_a,
            purchase_date=date(2020, 1, 1),
            age=age,
            breed=breed,
            color=color,
        )
        self.cow_b = Cow.objects.create(
            client=self.client_b,
            purchased_by=self.owner_b,
            purchase_date=date(2020, 1, 1),
            age=age,
            breed=breed,
            color=color,
        )
        action = Action.objects.create(name='Synthetic Action')
        self.event_b = Event.objects.create(
            client=self.client_b,
            recorded_by=self.owner_b,
            event_time=timezone.make_aware(datetime(2020, 1, 1)),
            cow=self.cow_b,
            action=action,
        )
        self.status_b = Status.objects.create(name='Bacterial Illness')
        self.health_record_b = HealthRecord.objects.create(
            client=self.client_b,
            recorded_by=self.owner_b,
            inspection_time=timezone.make_aware(datetime(2020, 1, 1)),
            cow=self.cow_b,
            status=self.status_b,
        )
        self.milk_b = Milk.objects.create(
            client=self.client_b,
            recorded_by=self.owner_b,
            milking_time=timezone.make_aware(datetime(2020, 1, 1)),
            cow=self.cow_b,
            gallons=7,
        )
        self.pasture_b = Pasture.objects.create(
            client=self.client_b,
            name='Farm B Pasture',
            url='https://example.test/farm-b-pasture',
        )
        Annual.objects.create(
            client=self.client_b,
            created_by=self.owner_b,
            year=2020,
        )
        self.client.force_authenticate(user=self.owner_a)

    def test_client_list_contains_only_the_authenticated_users_clients(self):
        response = self.client.get(reverse('assets:client-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        client_names = [item['name'] for item in response.data['results']]
        self.assertEqual(['Synthetic Farm A'], client_names)

    def test_unfiltered_cow_list_contains_only_the_authenticated_users_cows(
            self):
        response = self.client.get(reverse('assets:cow-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        cow_ids = [item['id'] for item in response.data['results']]
        self.assertEqual([self.cow_a.pk], cow_ids)

    def test_staff_can_access_all_tenants(self):
        self.owner_a.is_staff = True
        self.owner_a.save(update_fields=['is_staff'])
        self.client.force_authenticate(user=self.owner_a)

        response = self.client.get(reverse('assets:cow-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        cow_ids = [item['id'] for item in response.data['results']]
        self.assertCountEqual([self.cow_a.pk, self.cow_b.pk], cow_ids)

    def test_other_clients_cow_list_is_empty(self):
        response = self.client.get(
            reverse('assets:cow-list-client', kwargs={'pk': self.client_b.pk})
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data['results'])

    def test_other_clients_cow_detail_is_not_found(self):
        response = self.client.get(
            reverse('assets:cow-detail', kwargs={'pk': self.cow_b.pk})
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_clients_event_detail_is_not_found(self):
        response = self.client.get(
            reverse('assets:event-detail', kwargs={'pk': self.event_b.pk})
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_clients_health_record_detail_is_not_found(self):
        response = self.client.get(
            reverse(
                'assets:healthrecord-detail',
                kwargs={'pk': self.health_record_b.pk},
            )
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_clients_milk_detail_is_not_found(self):
        response = self.client.get(
            reverse('assets:milk-detail', kwargs={'pk': self.milk_b.pk})
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_clients_pasture_detail_is_not_found(self):
        response = self.client.get(
            reverse('assets:pasture-detail', kwargs={'pk': self.pasture_b.pk})
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_clients_cow_cannot_be_soft_deleted(self):
        response = self.client.delete(
            reverse('assets:cow-detail', kwargs={'pk': self.cow_b.pk})
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.cow_b.refresh_from_db()
        self.assertEqual(date(2100, 12, 31), self.cow_b.sell_date)

    def test_user_cannot_create_cow_for_another_clients_farm(self):
        data = {
            'client': self.client_b.name,
            'purchased_by': self.owner_b.username,
            'purchase_date': '2020-01-01',
            'age': self.cow_b.age.name,
            'breed': self.cow_b.breed.name,
            'color': self.cow_b.color.name,
        }

        response = self.client.post(
            reverse('assets:cow-list'),
            data,
            format='json',
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(2, Cow.objects.count())

    def test_user_cannot_move_a_cow_to_another_clients_farm(self):
        data = {
            'client': self.client_b.name,
            'purchased_by': self.owner_a.username,
            'purchase_date': '2020-01-01',
            'age': self.cow_a.age.name,
            'breed': self.cow_a.breed.name,
            'color': self.cow_a.color.name,
            'sell_date': '2100-12-31',
        }

        response = self.client.put(
            reverse('assets:cow-detail', kwargs={'pk': self.cow_a.pk}),
            data,
            format='json',
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.cow_a.refresh_from_db()
        self.assertEqual(self.client_a, self.cow_a.client)

    def test_other_clients_event_list_is_empty(self):
        response = self.client.get(
            reverse(
                'assets:event-list-client',
                kwargs={'pk': self.client_b.pk},
            )
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data['results'])

    def test_other_clients_annual_summary_is_empty(self):
        response = self.client.get(
            reverse(
                'summary:annual-client-year',
                kwargs={'pk': self.client_b.pk, 'year': 2020},
            )
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)

    def test_monthly_health_aggregate_excludes_other_clients(self):
        response = self.client.get(
            reverse(
                'assets:healthrecord-illness-summary-month',
                kwargs={'year': 2020, 'month': '01'},
            )
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, response.data[0]['status'])

    def test_monthly_milk_aggregate_excludes_other_clients(self):
        response = self.client.get(
            reverse(
                'assets:milk-summary-month',
                kwargs={'year': 2020, 'month': '01'},
            )
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNone(response.data[0]['gallons'])

    def test_user_list_does_not_disclose_other_users(self):
        response = self.client.get(reverse('assets:user-list'))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        usernames = [item['username'] for item in response.data['results']]
        self.assertEqual([self.owner_a.username], usernames)
