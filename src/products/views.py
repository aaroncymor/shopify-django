# Built-in
import os
import binascii

# Django
from django.shortcuts import render, redirect
from django.conf import settings

# 3rd Party
import shopify
from shopify import Session as ShopifySession

# Local
from .forms import ProductForm


# Create your views here.
def index(request):
    # reference: https://github.com/Shopify/shopify_python_api

    if request.method == 'GET':
        try:
            # hmac, #tstamp
            hmac = request.GET.get('hmac', None)
            tstamp = request.GET.get('timestamp', None)

            ShopifySession.setup(
                api_key=settings.SHOPIFY_API_CLIENT,
                secret=settings.SHOPIFY_API_SECRET
            )
            state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
            redirect_uri = "http://localhost:8012/products/redirected"
            scopes = ['read_products', 'read_orders']

            newSession = ShopifySession(
                settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION)
            auth_url = newSession.create_permission_url(scopes, redirect_uri)
            print("AUTH URL", auth_url)

            print("REDIRECTING")
            return redirect(auth_url)
            #access_token = ShopifySession(shop_url, api_version).request_token({"hmac": hmac, })
        except KeyError as ke:
            print("KeyError", ke)

    return render(request, 'products/index.html')


def redirected(request, *args, **kwargs):
    print("REDIRECTED REQUEST", request)
    print("REDIRECTED KWARGS", args)
    print("REDIRECTED ARGS", kwargs)
    request_params = request.GET.copy()

    print("REQUEST PARAMS", request_params)

    session = ShopifySession(
        settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION)
    access_token = session.request_token(request_params)

    print("ACCESS TOKEN", access_token)

    newSession = ShopifySession(
        settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION, access_token)
    shopify.ShopifyResource.activate_session(newSession)

    shop = shopify.Shop.current()
    products = shopify.Product.find()
    print(products)

    return render(request, 'products/product_list.html', context={
        "products": products
    })


def product_form_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            # Handle form data, e.g., save to database
            title = form.cleaned_data['title']
            body_title = form.cleaned_data['body_html']
            vendor = form.cleaned_data['vendor']
            product_type = form.cleaned_data['product_type']
            status = form.cleaned_data['status']

            # do something with data
            print("INSERTING...")

            return render(request, 'products/product_form_success.html')
        else:
            # Handle form errors
            return render(request, 'products/product_create.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'products/product_create.html', {'form': form})
