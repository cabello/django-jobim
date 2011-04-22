from django.test import TestCase

from jobim.tests.helpers import add_test_product


class JobimModelsTest(TestCase):
    def test_product_status(self):
        from jobim.models import Bid

        product = add_test_product()
        self.assertEquals('Waiting bid', product.status())

        bid = Bid(
            product=product,
            amount=100,
            email='john@buyer.com',
            accepted=False)
        bid.save()
        self.assertEquals('Waiting bid', product.status())

        bid.accepted = True
        bid.save()
        self.assertEquals('Current bid: U$ 100', product.status())

        product.sold = True
        product.save()
        self.assertEquals('Sold', product.status())

    def test_product_avaiable(self):
        from jobim.models import Product

        product = add_test_product()
        self.assertTrue(product in Product.available.all())

        product.sold = True
        product.save()

        self.assertFalse(product in Product.available.all())
