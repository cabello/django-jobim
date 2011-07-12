from django.core.urlresolvers import reverse
from django.test import TestCase

from jobim.tests.helpers import add_test_product


class JobimViewsTest(TestCase):
    fixtures = ['sites', 'stores']

    def add_url_kwargs(self, **kwargs):
        self.url_kwargs['kwargs'].update(kwargs)

    def setUp(self):
        from jobim.models import Store

        self.store = Store.objects.get(pk=1)
        self.url_kwargs = {'kwargs': {'store_url': self.store.url}}

    def test_about(self):
        response = self.client.get(reverse('jobim:about', **self.url_kwargs))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/about.html')
        self.assertContains(response, 'Ele serve para sabermos quanto as pess')

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

    def test_products_list(self):
        products_url = reverse('jobim:product_list', **self.url_kwargs)
        response = self.client.get(products_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response, 'jobim/product_list.html')
        self.assertEqual(0, len(response.context['products']))

        product = add_test_product()
        response = self.client.get(products_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['products']))
        self.assertTrue(product in response.context['products'])

        product.status = 'SOLD'
        product.save()
        response = self.client.get(products_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.context['products']))
        self.assertFalse(product in response.context['products'])

    def test_product_detail(self):
        self.add_url_kwargs(product_slug='pragmatic-programmer')
        product_detail_url = reverse('jobim:product_detail', **self.url_kwargs)

        response = self.client.get(product_detail_url)
        self.assertEqual(404, response.status_code)

        product = add_test_product()
        response = self.client.get(product_detail_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/product_detail.html')

        product.status = 'SOLD'
        product.save()
        response = self.client.get(product_detail_url)
        self.assertEqual(404, response.status_code)

    def test_bid(self):
        from jobim.models import Bid
        from jobim.views import BID_SUCCESS, BID_ERROR

        self.add_url_kwargs(product_slug='pragmatic-programmer')
        product_detail_url = reverse('jobim:product_detail', **self.url_kwargs)
        bid_url = reverse('jobim:product_bid', **self.url_kwargs)
        product = add_test_product()

        response = self.client.post(
            bid_url,
            {'amount': 350, 'email': 'john@buyer.com'},
            follow=True)
        self.assertRedirects(response, product_detail_url)
        self.assertContains(response, BID_SUCCESS)
        self.assertEquals(1, Bid.objects.count())

        response = self.client.post(bid_url)
        self.assertTemplateUsed(response, 'jobim/product_detail.html')
        self.assertFalse(response.context['bid_form'].is_valid())
        self.assertContains(response, BID_ERROR)

        response = self.client.get(bid_url)
        self.assertRedirects(response, product_detail_url)

        product.status = 'SOLD'
        product.save()
        response = self.client.post(
            bid_url,
            {'amount': 370, 'email': 'doe@buyer.com'})
        self.assertEqual(404, response.status_code)
