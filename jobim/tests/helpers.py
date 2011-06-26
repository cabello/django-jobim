def add_test_store():
    from jobim.models import Store

    store = Store(
        name='Manoel Cowboy',
        slogan='Manoel is selling everything! Enjoy.',
        url='manoel',
        email='manoelcowboy@mail.com',
        about_content='About this site')
    store.save()

    return store


def add_test_category():
    from jobim.models import Category

    category = Category(name='Books', slug='books')
    category.save()

    return category


def add_test_product(store=None):
    from jobim.models import Product, Category

    if store is None:
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
