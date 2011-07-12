def add_test_product(store=None):
    from jobim.models import Product, Store

    store = Store.objects.get(pk=1)

    product = Product(
        store=store,
        name='The Pragmatic Programmer',
        slug='pragmatic-programmer',
        description='From Journeyman to master',
        status='AVLB')
    product.save()

    return product
