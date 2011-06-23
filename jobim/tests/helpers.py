def add_test_store():
    from jobim.models import Store

    store = Store(
        name='Manoel Cowboy',
        slogan='Manoel is selling everything! Enjoy.',
        url='manoel')
    store.save()

    return store

def add_test_product():
    from jobim.models import Product, Category

    store = add_test_store()

    category = Category.objects.get(slug='books')
    product = Product(
        store=store,
        name='The Pragmatic Programmer',
        slug='pragmatic-programmer',
        description='From Journeyman to master',
        category=category,
        sold=False)
    product.save()

    return product
