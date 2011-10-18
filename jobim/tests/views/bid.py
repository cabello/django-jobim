from django.core.urlresolvers import reverse
from django.test import TestCase

from jobim.tests.helpers import add_product, ViewTestCase


class BidViewTest(ViewTestCase):

    def setUp(self):
        super(BidViewTest, self).setUp()

        self.add_url_kwargs(product_slug='pragmatic-programmer')
        self.product_detail_url = reverse('jobim:product_detail', **self.url_kwargs)
        self.bid_url = reverse('jobim:product_bid', **self.url_kwargs)
        self.product = add_product()

    def test_accept_valid_data(self):
        from jobim.models import Bid
        from jobim.views import BID_SUCCESS, BID_ERROR

        response = self.client.post(
            self.bid_url,
            {'amount': 350, 'email': 'john@buyer.com'},
            follow=True)
        self.assertRedirects(response, self.product_detail_url)
        self.assertContains(response, BID_SUCCESS)
        self.assertEquals(1, Bid.objects.count())

    def test_uses_right_template(self):
        response = self.client.post(self.bid_url)
        self.assertTemplateUsed(response, 'jobim/product_detail.html')

    def test_validates_form(self):
        from jobim.views import BID_ERROR

        response = self.client.post(self.bid_url)
        self.assertFalse(response.context['bid_form'].is_valid())
        self.assertContains(response, BID_ERROR)

    def test_do_not_allow_bid_on_sold_product(self):
        response = self.client.get(self.bid_url)
        self.assertRedirects(response, self.product_detail_url)

        self.product.status = 'SOLD'
        self.product.save()
        response = self.client.post(
            self.bid_url,
            {'amount': 370, 'email': 'doe@buyer.com'})
        self.assertEqual(404, response.status_code)
