from django.test import TestCase

from jobim.tests.helpers import add_test_product


class JobimAdminTest(TestCase):
    def test_accept_bid(self):
        from jobim.admin import BidAdmin
        from jobim.models import Bid

        product = add_test_product()
        bid = Bid(product=product, value=30)
        bid.save()
        self.assertFalse(bid.accepted)
        queryset = Bid.objects.all()
        bid_admin = BidAdmin(Bid, None)
        bid_admin.accept_bid(None, queryset)
        bid = Bid.objects.get(pk=bid.pk)
        self.assertTrue(bid.accepted)
