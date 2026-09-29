from django.contrib.auth.models import User
from django.test import TestCase

from tools.create_user import create_user
from tools.disable_demo_accounts import disable_accounts


class TestUserCreationTool(TestCase):
    def test_default_account_is_not_privileged(self):
        user = create_user(
            'Synthetic',
            'User',
            'synthetic@example.test',
            'synthetic-user',
            'test-password',
        )

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('test-password'))

    def test_staff_access_must_be_explicit(self):
        user = create_user(
            None,
            None,
            'staff@example.test',
            'synthetic-staff',
            'test-password',
            staff=True,
        )

        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser_access_must_be_explicit(self):
        user = create_user(
            None,
            None,
            'admin@example.test',
            'synthetic-admin',
            'test-password',
            superuser=True,
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_duplicate_usernames_are_rejected(self):
        User.objects.create_user(
            username='existing-user',
            email='existing@example.test',
            password='test-password',
        )

        with self.assertRaisesMessage(ValueError, 'username already exists'):
            create_user(
                None,
                None,
                'duplicate@example.test',
                'existing-user',
                'test-password',
            )

    def test_short_passwords_are_rejected(self):
        with self.assertRaisesMessage(
                ValueError, 'password must be at least 12 characters'):
            create_user(
                None,
                None,
                'short@example.test',
                'short-password-user',
                'short',
            )

    def test_demo_account_disabling_is_dry_run_by_default(self):
        user = User.objects.create_user(
            username='exposed-demo-user',
            password='test-password',
            is_staff=True,
            is_superuser=True,
        )

        users = disable_accounts(['exposed-demo-user'])

        self.assertEqual([user.pk], [result.pk for result in users])
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('test-password'))

    def test_demo_account_disabling_removes_access_and_password(self):
        user = User.objects.create_user(
            username='exposed-demo-user',
            password='test-password',
            is_staff=True,
            is_superuser=True,
        )

        disable_accounts(['exposed-demo-user'], apply=True)

        user.refresh_from_db()
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.has_usable_password())
