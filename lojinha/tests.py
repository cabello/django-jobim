from django.test import TestCase


def add_test_product():
    from lojinha.models import Product, Category

    category = Category.objects.get(slug='livros')
    product = Product(
        name='The Pragmatic Programmer',
        slug='pragmatic-programmer',
        description='from jouneryman to master',
        category=category,
        sold=False
    )
    product.save()

    return product


class LojinhaAdminTest(TestCase):
    def test_accept_bid(self):
        from lojinha.admin import BidAdmin
        from lojinha.models import Bid

        product = add_test_product()
        bid = Bid(product=product, value=30)
        bid.save()
        self.assertFalse(bid.accepted)
        queryset = Bid.objects.all()
        bid_admin = BidAdmin(Bid, None)
        bid_admin.accept_bid(None, queryset)
        bid = Bid.objects.get(pk=bid.pk)
        self.assertTrue(bid.accepted)


class LojinhaModelsTest(TestCase):
    def test_product_status(self):
        from lojinha.models import Bid

        product = add_test_product()
        self.assertEquals('Esperando oferta', product.status())

        bid = Bid(
            product=product,
            value=100,
            mail='john@buyer.com',
            accepted=False
        )
        bid.save()
        self.assertEquals('Esperando oferta', product.status())

        bid.accepted = True
        bid.save()
        self.assertEquals('Maior oferta: R$ 100', product.status())

        product.sold = True
        product.save()
        self.assertEquals('Vendido', product.status())


class LojinhaViewsTest(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertRedirects(response, 'sobre')

    def test_about(self):
        response = self.client.get('/sobre')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'about.txt')
        self.assertTemplateUsed(response, 'about.html')

    def test_contact(self):
        from django.conf import settings
        from django.core import mail

        from lojinha.models import Contact

        response = self.client.get('/contato')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'contact.html')

        response = self.client.post('/contato')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertFalse(response.context['contact_form'].is_valid())
        self.assertFormError(
            response,
            'contact_form',
            'email',
            'This field is required.'
        )

        self.assertEqual(0, Contact.objects.count())
        response = self.client.post(
            '/contato',
            {'email': 'john@buyer.com'}
        )
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'contact_success.html')
        self.assertEqual(1, Contact.objects.count())

        mail.outbox = []
        contact_form = {
            'name': 'John',
            'email': 'john@buyer.com',
            'phone': '555-1234',
            'subject': 'How much for the box?',
            'message': 'I saw prrety box in your store...',
        }
        response = self.client.post(
            '/contato',
            contact_form
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(mail.outbox))
        message = mail.outbox[0]
        self.assertEqual(settings.CONTACT_EMAIL, message.to[0])
        self.assertEqual('john@buyer.com', message.from_email)
        self.assertTemplateUsed(response, 'contact_subject.txt')
        self.assertTemplateUsed(response, 'contact_message.txt')

    def test_products_by_category(self):
        response = self.client.get('/carros')
        self.assertEqual(404, response.status_code)

        response = self.client.get('/livros')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lojinha/products_by_category.html')
        self.assertEqual(0, len(response.context['products']))

        product = add_test_product()
        response = self.client.get('/livros')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['products']))
        self.assertTrue(product in response.context['products'])

        product.sold = True
        product.save()
        response = self.client.get('/livros')
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.context['products']))
        self.assertFalse(product in response.context['products'])

    def test_product_view(self):
        response = self.client.get('/livros/pragmatic-programmer')
        self.assertEqual(404, response.status_code)

        product = add_test_product()
        response = self.client.get('/livros/pragmatic-programmer')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'lojinha/product_view.html')

        product.sold = True
        product.save()
        response = self.client.get('/livros/pragmatic-programmer')
        self.assertEqual(404, response.status_code)

    def test_bid(self):
        from lojinha.models import Bid
        from lojinha.views import BID_SUCCESS, BID_ERROR

        add_test_product()
        response = self.client.post(
            '/livros/pragmatic-programmer/lance',
            {'value': 350, 'mail': 'john@buyer.com'},
            follow=True
        )
        self.assertRedirects(response, '/livros/pragmatic-programmer')
        self.assertContains(response, BID_SUCCESS)
        self.assertEquals(1, Bid.objects.count())

        response = self.client.post('/livros/pragmatic-programmer/lance')
        self.assertTemplateUsed(response, 'lojinha/product_view.html')
        self.assertFalse(response.context['bid_form'].is_valid())
        self.assertContains(response, BID_ERROR)

        response = self.client.get('/livros/pragmatic-programmer/lance')
        self.assertRedirects(response, '/livros/pragmatic-programmer')
