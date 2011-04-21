from django.test import TestCase

from jobim.tests.helpers import add_test_product


class JobimModelsTest(TestCase):
    def test_product_status(self):
        from jobim.models import Bid

        product = add_test_product()
        self.assertEquals('Esperando oferta', product.status())

        bid = Bid(
            product=product,
            amount=100,
            email='john@buyer.com',
            accepted=False)
        bid.save()
        self.assertEquals('Esperando oferta', product.status())

        bid.accepted = True
        bid.save()
        self.assertEquals('Maior oferta: R$ 100', product.status())

        product.sold = True
        product.save()
        self.assertEquals('Vendido', product.status())
