from django.core.urlresolvers import reverse
from django.test import TestCase

from lojinha.tests.helpers import add_test_product


class LojinhaViewsTest(TestCase):
    def test_index(self):
        response = self.client.get(reverse('leilao_index'))
        self.assertRedirects(response, reverse('leilao_sobre'))

    def test_about(self):
        response = self.client.get(reverse('leilao_sobre'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'about.txt')
        self.assertTemplateUsed(response, 'about.html')

    def test_contact(self):
        from django.conf import settings
        from django.core import mail

        from lojinha.models import Contact

        response = self.client.get(reverse('leilao_contato'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'contact.html')

        response = self.client.post(reverse('leilao_contato'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertFalse(response.context['contact_form'].is_valid())
        self.assertFormError(
            response,
            'contact_form',
            'email',
            'This field is required.')

        self.assertEqual(0, Contact.objects.count())
        response = self.client.post(
            '/contato',
            {'email': 'john@buyer.com'})
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'contact_success.html')
        self.assertEqual(1, Contact.objects.count())

        mail.outbox = []
        contact_form = {
            'name': 'John',
            'email': 'john@buyer.com',
            'phone': '555-1234',
            'subject': 'How much for the box?',
            'message': 'I saw prrety box in your store...'}
        response = self.client.post(
            reverse('leilao_contato'),
            contact_form)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(mail.outbox))
        message = mail.outbox[0]
        self.assertEqual(settings.CONTACT_EMAIL, message.to[0])
        self.assertEqual('john@buyer.com', message.from_email)
        self.assertTemplateUsed(response, 'contact_subject.txt')
        self.assertTemplateUsed(response, 'contact_message.txt')

    def test_products_by_category(self):
        response = self.client.get('/carros')
        self.assertEqual(404, response.status_code)

        response = self.client.get(reverse('leilao_livros'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lojinha/products_by_category.html')
        self.assertEqual(0, len(response.context['products']))

        product = add_test_product()
        response = self.client.get(reverse('leilao_livros'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['products']))
        self.assertTrue(product in response.context['products'])

        product.sold = True
        product.save()
        response = self.client.get(reverse('leilao_livros'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.context['products']))
        self.assertFalse(product in response.context['products'])

    def test_product_view(self):
        product_view_url = reverse(
            'leilao_product_view',
            kwargs={
                'category_slug': 'livros',
                'product_slug': 'pragmatic-programmer'})

        response = self.client.get(product_view_url)
        self.assertEqual(404, response.status_code)

        product = add_test_product()
        response = self.client.get(product_view_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lojinha/product_view.html')

        product.sold = True
        product.save()
        response = self.client.get(product_view_url)
        self.assertEqual(404, response.status_code)

    def test_bid(self):
        from lojinha.models import Bid
        from lojinha.views import BID_SUCCESS, BID_ERROR

        url_args = {
            'category_slug': 'livros',
            'product_slug': 'pragmatic-programmer'}
        product_view_url = reverse('leilao_product_view', kwargs=url_args)
        bid_url = reverse('leilao_product_bid', kwargs=url_args)
        add_test_product()

        response = self.client.post(
            bid_url,
            {'value': 350, 'mail': 'john@buyer.com'},
            follow=True)
        self.assertRedirects(response, product_view_url)
        self.assertContains(response, BID_SUCCESS)
        self.assertEquals(1, Bid.objects.count())

        response = self.client.post(bid_url)
        self.assertTemplateUsed(response, 'lojinha/product_view.html')
        self.assertFalse(response.context['bid_form'].is_valid())
        self.assertContains(response, BID_ERROR)

        response = self.client.get(bid_url)
        self.assertRedirects(response, product_view_url)
