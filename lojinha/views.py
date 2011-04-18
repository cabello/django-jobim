from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render_to_response, \
                             redirect
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.views.generic.simple import direct_to_template

from lojinha.forms import ContactForm, BidForm
from lojinha.models import Category, Product, Bid


def index(request):
    return redirect('leilao_sobre')


def about(request):
    about_content = get_template('about.txt').render(Context())
    return render_to_response(
        'about.html',
        {'about_content': about_content},
        context_instance=RequestContext(request)
    )


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            mail_context = Context(contact_form.cleaned_data)
            send_mail(
                get_template('contact_subject.txt').render(mail_context),
                get_template('contact_message.txt').render(mail_context),
                contact_form.cleaned_data['email'],
                [settings.CONTACT_EMAIL]
            )
            return direct_to_template(request, 'contact_success.html')
    else:
        contact_form = ContactForm()

    contact_email = settings.CONTACT_EMAIL
    return render_to_response(
        'contact.html',
        {'contact_form': contact_form, 'contact_email': contact_email},
        context_instance=RequestContext(request)
    )


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, sold=False)
    return render_to_response(
        'lojinha/products_by_category.html',
        {'category': category, 'products': products},
        context_instance=RequestContext(request)
     )


def product_view(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, sold=False)
    photos = product.photo_set.all()
    bid_form = BidForm(auto_id='item_bid_%s')
    return render_to_response(
        'lojinha/product_view.html',
        {'product': product, 'photos': photos, 'bid_form': bid_form},
        context_instance=RequestContext(request)
    )

BID_SUCCESS = 'Recebemos sua oferta, se ela for interessante entraremos em \
               contato. :D'
BID_ERROR = 'Ocorreram problemas com o preenchimento da oferta, \
             corrija os erros abaixo.'


def bid(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, sold=False)
    photos = product.photo_set.all()
    if request.method == 'POST':
        bid_form = BidForm(request.POST, auto_id='item_bid_%s')
        if bid_form.is_valid():
            new_bid = Bid()
            new_bid.product = product
            new_bid.value = bid_form.cleaned_data['amount']
            new_bid.mail = bid_form.cleaned_data['email']
            new_bid.save()
            messages.success(request, BID_SUCCESS)
            return redirect(
                'leilao_product_view',
                category_slug,
                product_slug
            )
        else:
            messages.warning(request, BID_ERROR)
            return render_to_response(
                'lojinha/product_view.html',
                {
                    'product': product,
                    'photos': photos,
                    'bid_form': bid_form
                },
                context_instance=RequestContext(request)
            )
    else:
        return redirect(
            'leilao_product_view',
            category_slug,
            product_slug
        )
