from django.test import TestCase

from jobim.models import Photo
from jobim.tests.helpers import add_product

class PhotoModelTest(TestCase):
    fixtures = ['sites', 'stores']

    def test_has_unicode(self):
        product = add_product()
        photo = Photo(product=product)
        photo.save()

        self.assertEqual('The Pragmatic Programmer #1', str(photo))

