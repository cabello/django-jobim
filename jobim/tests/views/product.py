from django.core.urlresolvers import reverse

from jobim.tests.helpers import add_product, ViewTestCase


class ProductDetailViewTest(ViewTestCase):

    def setUp(self):
        super(ProductDetailViewTest, self).setUp()

        self.add_url_kwargs(product_slug='pragmatic-programmer')
        self.product_detail_url = reverse(
            'jobim:product_detail', **self.url_kwargs)

    def test_shows_not_found_page_for_non_existent_product(self):
        response = self.client.get(self.product_detail_url)
        self.assertEqual(404, response.status_code)

    def test_uses_right_template(self):
        product = add_product()
        response = self.client.get(self.product_detail_url)
        self.assertTemplateUsed(response, 'jobim/product_detail.html')

    def test_show_product_details(self):
        product = add_product()
        response = self.client.get(self.product_detail_url)
        self.assertEqual(200, response.status_code)

    def test_show_details_of_sold_product_without_bid_form(self):
        product = add_product(status='SOLD')
        response = self.client.get(self.product_detail_url)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['bid_form'])


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

    def test_do_not_show_draft_products(self):
        product = add_product('DRFT')
        response = self.client.get(self.products_url)

        self.assertEqual(0, len(response.context['products']))
        self.assertFalse(product in response.context['products'])
