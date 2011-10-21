from django.test import TestCase

from jobim.models import Store

class StoreModelTest(TestCase):

    def test_has_unicode(self):
        store = Store(name='Manoel Cowboy', url='manoel')

        self.assertEqual('manoel', str(store))
