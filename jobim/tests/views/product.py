from django.core.urlresolvers import reverse
from django.test import TestCase

from jobim.tests.helpers import add_test_product


class ProductViewsTest(TestCase):
    fixtures = ['sites', 'stores']

    def add_url_kwargs(self, **kwargs):
        self.url_kwargs['kwargs'].update(kwargs)

    def setUp(self):
        from jobim.models import Store

        self.store = Store.objects.get(pk=1)
        self.url_kwargs = {'kwargs': {'store_url': self.store.url}}

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
