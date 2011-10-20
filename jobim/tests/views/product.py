from django.core.urlresolvers import reverse

from jobim.tests.helpers import add_product, ViewTestCase


class ProductDetailViewTest(ViewTestCase):

    def test_works(self):
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


class ProductListViewTest(ViewTestCase):

    def setUp(self):
        super(ProductListViewTest, self).setUp()

        self.products_url = reverse('jobim:product_list', **self.url_kwargs)
        self.response = self.client.get(self.products_url)

    def test_exists(self):
        self.assertEqual(200, self.response.status_code)

    def test_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'jobim/product_list.html')

    def test_shows_nothing_when_store_is_empty(self):
        self.assertEmpty(self.response.context['products'])

    def test_shows_available_products(self):
        product = add_product()
        response = self.client.get(self.products_url)

        self.assertEqual(1, len(response.context['products']))
        self.assertTrue(product in response.context['products'])

    def test_shows_even_sold_products(self):
        product = add_product('SOLD')
        response = self.client.get(self.products_url)

        self.assertEqual(1, len(response.context['products']))
        self.assertTrue(product in response.context['products'])
