from datetime import date

from django.contrib.auth.models import User
from django.test import Client as DjangoClient
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from assets.models import Client


class TestUIAuthentication(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='synthetic-ui-user',
            password='test-password',
        )
        self.client_record = Client.objects.create(
            user=self.user,
            name='Synthetic UI Farm',
            join_date=date(2020, 1, 1),
        )

    def test_logged_in_endpoint_requires_authentication(self):
        response = self.client.get(reverse('ui_logged_in'))

        self.assertEqual(302, response.status_code)
        self.assertIn('/login/', response['Location'])

    def test_logged_in_endpoint_reports_only_the_current_users_clients(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('ui_logged_in'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [{'id': self.client_record.pk, 'name': self.client_record.name}],
            response.json()['user']['clients'],
        )

    def test_logged_in_endpoint_supports_users_without_a_client(self):
        user_without_client = User.objects.create_user(
            username='no-client-user',
            password='test-password',
        )
        self.client.force_login(user_without_client)

        response = self.client.get(reverse('ui_logged_in'))

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json()['user']['clients'])
        self.assertIsNone(response.json()['user']['client'])

    def test_logout_requires_post_and_clears_the_session(self):
        self.client.force_login(self.user)

        get_response = self.client.get(reverse('ui_logout'))
        post_response = self.client.post(reverse('ui_logout'))

        self.assertEqual(405, get_response.status_code)
        self.assertEqual(200, post_response.status_code)
        logged_in_response = self.client.get(reverse('ui_logged_in'))
        self.assertEqual(302, logged_in_response.status_code)

    def test_logout_enforces_csrf_for_session_authentication(self):
        client = DjangoClient(enforce_csrf_checks=True)
        client.force_login(self.user)

        blocked = client.post(reverse('ui_logout'))
        self.assertEqual(403, blocked.status_code)

        csrf_response = client.get(reverse('ui_login'))
        csrf_token = csrf_response.cookies['csrftoken'].value
        logged_out = client.post(
            reverse('ui_logout'),
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(200, logged_out.status_code)
        self.assertEqual('', client.cookies['sessionid'].value)

    @override_settings(CSRF_TRUSTED_ORIGINS=['http://testserver'])
    def test_login_accepts_trusted_same_origin_csrf_post(self):
        client = DjangoClient(enforce_csrf_checks=True)
        login_page = client.get(reverse('ui_login'))
        csrf_token = login_page.cookies['csrftoken'].value

        response = client.post(
            reverse('login'),
            {
                'username': self.user.username,
                'password': 'test-password',
                'csrfmiddlewaretoken': csrf_token,
                'next': reverse('ui_logged_in'),
            },
            HTTP_ORIGIN='http://testserver',
        )

        self.assertEqual(302, response.status_code)
        self.assertEqual(
            200,
            client.get(reverse('ui_logged_in')).status_code,
        )
