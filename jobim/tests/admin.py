from django.test import TestCase

from jobim.tests.helpers import add_product


class JobimAdminTest(TestCase):
    fixtures = ['sites', 'stores']

    def test_accept_bid(self):
        from jobim.admin import BidAdmin
        from jobim.models import Bid

        product = add_product()
        bid = Bid(product=product, amount=30)
        bid.save()
        self.assertFalse(bid.accepted)

        queryset = Bid.objects.all()
        bid_admin = BidAdmin(Bid, None)
        bid_admin.accept_bid(None, queryset)
        bid = Bid.objects.get(pk=bid.pk)
        self.assertTrue(bid.accepted)
