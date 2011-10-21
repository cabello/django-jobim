from django.test import TestCase

from jobim.models import Contact, Store


class ContactModelTest(TestCase):
    fixtures = ['stores']

    def test_has_unicode(self):
        store = Store.objects.get(pk=1)
        contact = Contact(
            store=store,
            name='Johnny Bravo',
            email='johnny@begood.com',
            subject='Interest in stove')

        self.assertEqual(
            'Johnny Bravo <johnny@begood.com> - Interest in stove',
            str(contact))
