from django.test import TestCase

from jobim.tests.helpers import add_product


class JobimModelsTest(TestCase):
    fixtures = ['sites', 'stores']

    def test_product_status(self):
        from jobim.models import Bid

        product = add_product()
        self.assertEquals('Waiting bid', product.bid_status())

        bid = Bid(
            product=product,
            amount=100,
            email='john@buyer.com',
            accepted=False)
        bid.save()
        self.assertEquals('Waiting bid', product.bid_status())

        bid.accepted = True
        bid.save()
        self.assertEquals('Current bid: U$ 100', product.bid_status())

        product.status = 'SOLD'
        product.save()
        self.assertEquals('Sold', product.bid_status())

    def test_product_avaiable(self):
        from jobim.models import Product

        product = add_product()
        self.assertTrue(product in Product.available.all())

        product.status = 'SOLD'
        product.save()

        self.assertFalse(product in Product.available.all())

    def test_product_sold(self):
        from jobim.models import Product

        product = add_product()
        self.assertFalse(product in Product.sold.all())

        product.status = 'SOLD'
        product.save()

        self.assertTrue(product in Product.sold.all())
