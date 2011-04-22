from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.views.generic.simple import direct_to_template

from jobim.forms import BidForm, ContactForm
from jobim.models import Bid, Category, Product


BID_SUCCESS = 'Recebemos sua oferta, se ela for interessante entraremos em \
               contato. :D'
BID_ERROR = 'Ocorreram problemas com o preenchimento da oferta, \
             corrija os erros abaixo.'


def index(request):
    return redirect('jobim_about')


def about(request):
    about_content = get_template('jobim/about.txt').render(Context())
    return render_to_response(
        'jobim/about.html',
        {'about_content': about_content},
        context_instance=RequestContext(request))


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return direct_to_template(request, 'contact_success.html')
    else:
        contact_form = ContactForm()

    contact_email = settings.CONTACT_EMAIL
    return render_to_response(
        'contact.html',
        {'contact_form': contact_form, 'contact_email': contact_email},
        context_instance=RequestContext(request))


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.available.filter(category=category)
    return render_to_response(
        'jobim/products_by_category.html',
        {'category': category, 'products': products},
        context_instance=RequestContext(request))


def product_view(request, category_slug, product_slug):
    product = get_object_or_404(Product.available, slug=product_slug)
    photos = product.photo_set.all()
    bid_form = BidForm(auto_id='item_bid_%s')
    return render_to_response(
        'jobim/product_view.html',
        {'product': product, 'photos': photos, 'bid_form': bid_form},
        context_instance=RequestContext(request))


def bid(request, category_slug, product_slug):
    if request.method == 'POST':
        product = get_object_or_404(Product.available, slug=product_slug)
        bid = Bid(product=product)
        bid_form = BidForm(request.POST, auto_id='item_bid_%s', instance=bid)
        if bid_form.is_valid():
            bid_form.save(product)
            messages.success(request, BID_SUCCESS)
            return redirect('jobim_product_view', category_slug, product_slug)
        else:
            photos = product.photo_set.all()
            messages.warning(request, BID_ERROR)
            return render_to_response(
                'jobim/product_view.html',
                {'product': product, 'photos': photos, 'bid_form': bid_form},
                context_instance=RequestContext(request))
    else:
        return redirect('jobim_product_view', category_slug, product_slug)
