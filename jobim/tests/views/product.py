from django.core.urlresolvers import reverse

from jobim.tests.helpers import add_product, ViewTestCase


class ProductViewsTest(ViewTestCase):

    def test_list_view(self):
        products_url = reverse('jobim:product_list', **self.url_kwargs)
        response = self.client.get(products_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response, 'jobim/product_list.html')
        self.assertEqual(0, len(response.context['products']))

        product = add_product()
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

    def test_detail_view(self):
        self.add_url_kwargs(product_slug='pragmatic-programmer')
        product_detail_url = reverse('jobim:product_detail', **self.url_kwargs)

        response = self.client.get(product_detail_url)
        self.assertEqual(404, response.status_code)

        product = add_product()
        response = self.client.get(product_detail_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'jobim/product_detail.html')

        product.status = 'SOLD'
        product.save()
        response = self.client.get(product_detail_url)
        self.assertEqual(404, response.status_code)
