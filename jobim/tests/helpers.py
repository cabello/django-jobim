def add_test_product():
    from jobim.models import Product, Category

    category = Category.objects.get(slug='books')
    product = Product(
        name='The Pragmatic Programmer',
        slug='pragmatic-programmer',
        description='From Journeyman to master',
        category=category,
        sold=False)
    product.save()

    return product
