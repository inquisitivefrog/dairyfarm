from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class TestUserAPI(APITestCase):
    def setUp(self):
        self.url = reverse('user_create')
        self.data = {
            'username': 'new-user',
            'email': 'new-user@example.com',
            'password': 'a-long-test-password',
        }
        self.staff_user = User.objects.create_user(
            username='staff-user',
            password='staff-password',
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username='regular-user',
            password='regular-password',
        )
        self.target_user = User.objects.create_user(
            username='target-user',
            password='target-password',
        )

    def test_anonymous_user_cannot_create_accounts(self):
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertFalse(User.objects.filter(username='new-user').exists())

    def test_authenticated_non_staff_user_cannot_create_accounts(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertFalse(User.objects.filter(username='new-user').exists())

    def test_staff_user_can_create_non_staff_account(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        created_user = User.objects.get(username='new-user')
        self.assertTrue(created_user.check_password(self.data['password']))
        self.assertFalse(created_user.is_staff)
        self.assertFalse(created_user.is_superuser)

    def test_staff_cannot_create_account_with_short_password(self):
        self.client.force_authenticate(user=self.staff_user)
        data = dict(self.data, password='xylophone-1')

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(User.objects.filter(username='new-user').exists())

    def test_authenticated_non_staff_user_cannot_retrieve_user_details(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user_detail', kwargs={'pk': self.target_user.pk})

        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_staff_user_can_retrieve_user_details(self):
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('user_detail', kwargs={'pk': self.target_user.pk})

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.target_user.username, response.data['username'])
        self.assertNotIn('password', response.data)
