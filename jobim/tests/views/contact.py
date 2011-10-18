from django.core.urlresolvers import reverse
from django.test import TestCase

class ContactViewTest(TestCase):
    fixtures = ['sites', 'stores']

    def setUp(self):
        from jobim.models import Store

        self.store = Store.objects.get(pk=1)
        self.url_kwargs = {'kwargs': {'store_url': self.store.url}}

    def test_contact(self):
        from django.core import mail

        from jobim.models import Contact

        contact_url = reverse('jobim:contact', **self.url_kwargs)
        contact_success_url = reverse(
            'jobim:contact_success', **self.url_kwargs)

        response = self.client.get(contact_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/contact.html')

        response = self.client.post(contact_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/contact.html')
        self.assertFalse(response.context['contact_form'].is_valid())
        self.assertFormError(
            response,
            'contact_form',
            'email',
            'This field is required.')

        self.assertEqual(0, Contact.objects.count())
        response = self.client.post(
            contact_url,
            {'email': 'john@buyer.com'})
        self.assertRedirects(response, contact_success_url)
        self.assertEqual(1, Contact.objects.count())

        mail.outbox = []
        contact_form = {
            'name': 'John',
            'email': 'john@buyer.com',
            'phone': '555-1234',
            'subject': 'How much for the box?',
            'message': 'I saw prrety box in your store...'}
        response = self.client.post(
            contact_url,
            contact_form)
        self.assertRedirects(response, contact_success_url)
        self.assertEqual(1, len(mail.outbox))
        message = mail.outbox[0]
        self.assertEqual(self.store.email, message.to[0])
        self.assertEqual('john@buyer.com', message.from_email)
        self.assertTemplateUsed(response, 'jobim/contact_subject.txt')
        self.assertTemplateUsed(response, 'jobim/contact_message.txt')

    def test_contact_success(self):
        contact_success_url = reverse(
            'jobim:contact_success', **self.url_kwargs)

        response = self.client.get(contact_success_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/contact_success.html')
