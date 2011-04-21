def add_test_product():
    from lojinha.models import Product, Category

    category = Category.objects.get(slug='livros')
    product = Product(
        name='The Pragmatic Programmer',
        slug='pragmatic-programmer',
        description='from jouneryman to master',
        category=category,
        sold=False)
    product.save()

    return product
