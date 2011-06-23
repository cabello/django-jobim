from django.core.urlresolvers import reverse
from django.test import TestCase

from jobim.tests.helpers import (
    add_test_category, add_test_product, add_test_store)


class JobimViewsTest(TestCase):
    def test_index(self):
        store = add_test_store()
        store_dict = {'store_url': store.url}

        response = self.client.get(reverse('jobim:index', kwargs=store_dict))
        self.assertRedirects(
            response, reverse('jobim:about', kwargs=store_dict))

    def test_about(self):
        store = add_test_store()
        store_dict = {'store_url': store.url}

        response = self.client.get(reverse('jobim:about', kwargs=store_dict))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/about.txt')
        self.assertTemplateUsed(response, 'jobim/about.html')

    def test_contact(self):
        from django.conf import settings
        from django.core import mail

        from jobim.models import Contact

        store = add_test_store()
        store_dict = {'store_url': store.url}
        contact_url = reverse('jobim:contact', kwargs=store_dict)
        contact_success_url = reverse(
            'jobim:contact_success', kwargs=store_dict)

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
        self.assertEqual(settings.CONTACT_EMAIL, message.to[0])
        self.assertEqual('john@buyer.com', message.from_email)
        self.assertTemplateUsed(response, 'jobim/contact_subject.txt')
        self.assertTemplateUsed(response, 'jobim/contact_message.txt')

    def test_contact_success(self):
        store = add_test_store()
        store_dict = {'store_url': store.url}
        contact_success_url = reverse(
            'jobim:contact_success', kwargs=store_dict)

        response = self.client.get(contact_success_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/contact_success.html')

    def test_products_by_category(self):
        store = add_test_store()
        cars_url = reverse('jobim:category_view', kwargs={
            'store_url': store.url,
            'category_slug': 'cars'})
        response = self.client.get(cars_url)
        self.assertEqual(404, response.status_code)

        books_url = reverse('jobim:category_view', kwargs={
            'store_url': store.url,
            'category_slug': 'books'})
        response = self.client.get(books_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response, 'jobim/product_list_by_category.html')
        self.assertEqual(0, len(response.context['products']))

        product = add_test_product(store)
        response = self.client.get(books_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['products']))
        self.assertTrue(product in response.context['products'])

        product.sold = True
        product.save()
        response = self.client.get(books_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.context['products']))
        self.assertFalse(product in response.context['products'])

    def test_product_detail(self):
        store = add_test_store()
        product_detail_url = reverse(
            'jobim:product_detail',
            kwargs={
                'store_url': store.url,
                'category_slug': 'books',
                'product_slug': 'pragmatic-programmer'})

        response = self.client.get(product_detail_url)
        self.assertEqual(404, response.status_code)

        product = add_test_product(store)
        response = self.client.get(product_detail_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/product_detail.html')

        product.sold = True
        product.save()
        response = self.client.get(product_detail_url)
        self.assertEqual(404, response.status_code)

    def test_bid(self):
        from jobim.models import Bid
        from jobim.views import BID_SUCCESS, BID_ERROR

        store = add_test_store()
        url_args = {
            'store_url': store.url,
            'category_slug': 'books',
            'product_slug': 'pragmatic-programmer'}
        product_detail_url = reverse('jobim:product_detail', kwargs=url_args)
        bid_url = reverse('jobim:product_bid', kwargs=url_args)
        product = add_test_product(store)

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

        product.sold = True
        product.save()
        response = self.client.post(
            bid_url,
            {'amount': 370, 'email': 'doe@buyer.com'})
        self.assertEqual(404, response.status_code)
