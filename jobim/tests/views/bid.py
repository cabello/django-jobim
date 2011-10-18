from django.core.urlresolvers import reverse
from django.test import TestCase

from jobim.tests.helpers import add_test_product, ViewTestCase


class BidViewTest(ViewTestCase):

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
