from django.test import TestCase


def add_product(status='AVLB'):
    from jobim.models import Product, Store

    store = Store.objects.get(pk=1)

    product = Product(
        store=store,
        name='The Pragmatic Programmer',
        slug='pragmatic-programmer',
        description='From Journeyman to master',
        status=status)
    product.save()

    return product


class ViewTestCase(TestCase):
    fixtures = ['sites', 'stores']

    def assertEmpty(self, countable):
        return self.assertEqual(0, len(countable))

    def add_url_kwargs(self, **kwargs):
        self.url_kwargs['kwargs'].update(kwargs)

    def setUp(self):
        super(ViewTestCase, self).setUp()

        from jobim.models import Store

        self.store = Store.objects.get(pk=1)
        self.url_kwargs = {'kwargs': {'store_url': self.store.url}}
