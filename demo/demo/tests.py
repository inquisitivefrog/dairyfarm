from django.core import mail
from django.test import TestCase, override_settings


@override_settings(
    EMAIL_BACKEND=(
        'django.core.mail.backends.locmem.EmailBackend'))
class ContactViewTests(TestCase):
    def test_contact_page_renders_a_bound_form(self):
        response = self.client.get('/contact/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('contact_name', response.context['form'].fields)
        self.assertIn('csrftoken', response.cookies)

    def test_valid_contact_submission_sends_and_returns_to_contact_page(self):
        response = self.client.post('/contact/', {
            'contact_name': 'Demo User',
            'contact_email': 'demo@example.com',
            'content': 'This is a test message.',
        })

        self.assertRedirects(response, '/contact/')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['farmapp@localhost'])
        self.assertEqual(mail.outbox[0].reply_to, ['demo@example.com'])
