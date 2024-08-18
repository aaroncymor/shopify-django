# Built-in
from urllib.parse import urlencode

# Django
from django.shortcuts import render, redirect

# Local
from core import ShopifyClient

from .forms import ProductForm


# Create your views here.
def verify(request, *args, **kwargs):
    # reference: https://github.com/Shopify/shopify_python_api

    print("VERIFY REQUEST", request)
    print("VERIFY KWARGS", args)
    print("VERIFY ARGS", kwargs)
    request_params = request.GET.copy()
    print("VERIFY_PARAMS", request_params)

    if request.method == 'GET':
        print("GET METHOD")
        try:
            # # hmac, #tstamp
            # hmac = request.GET.get('hmac', None)
            # tstamp = request.GET.get('timestamp', None)
            #
            # ShopifySession.setup(
            #     api_key=settings.SHOPIFY_API_CLIENT,
            #     secret=settings.SHOPIFY_API_SECRET
            # )
            # state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
            # redirect_uri = "http://localhost:8012/products/redirected"
            # scopes = ['read_products', 'read_orders']
            #
            # newSession = ShopifySession(
            #     settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION)
            # auth_url = newSession.create_permission_url(scopes, redirect_uri)
            # print("AUTH URL", auth_url)
            #
            # print("REDIRECTING")

            redirect_uri = "http://localhost:8012/products/redirected"
            scopes = ['read_products', 'write_products', 'read_orders']

            shopify_client = ShopifyClient()
            auth_url = shopify_client.init_auth(scopes, redirect_uri)
            return redirect(auth_url)
            # return redirect('products:redirected')

        except KeyError as ke:
            print("KeyError", ke)
    else:
        print("NOT GET METHOD EYYYY")

    return render(request, 'products/index.html')


def redirected(request, *args, **kwargs):
    print("REDIRECTED REQUEST", request)
    print("REDIRECTED KWARGS", args)
    print("REDIRECTED ARGS", kwargs)
    request_params = request.GET.copy()

    print("REQUEST PARAMS", request_params)

    # session = ShopifySession(
    #     settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION)
    # access_token = session.request_token(request_params)
    #
    # print("ACCESS TOKEN", access_token)
    #
    # newSession = ShopifySession(
    #     settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION, access_token)
    # shopify.ShopifyResource.activate_session(newSession)
    #
    # shop = shopify.Shop.current()
    # products = shopify.Product.find()
    # print(products)

    shopify_client = ShopifyClient()
    shopify_client.activate_session(request_params)
    print("REDIRECTED ACCESS TOKEN", shopify_client.access_token)

    goto_page = request.session.get('goto', "")
    if goto_page == 'create_or_edit_product':
        print("GOING TO CREATE OR EDIT PRODUCT")
        return redirect('products:create_or_edit')

    # default goto is list_product
    print("GOING TO DEFAULT PAGE...")
    return redirect('products:list')


def product_list(request, *args, **kwargs):

    shopify_client = ShopifyClient()
    shopify_inst = shopify_client._shopify
    products = shopify_inst.Product.find()

    return render(request, 'products/product_list.html', context={
        "products": products
    })


def product_create_or_edit(request, *args, **kwargs):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            # Handle form data, e.g., save to database
            title = form.cleaned_data['title']
            body_html = form.cleaned_data['body_html']
            vendor = form.cleaned_data['vendor']
            product_type = form.cleaned_data['product_type']
            status = form.cleaned_data['status']

            # do something with data
            print("INSERTING...")
            print("TITLE", title)
            print("BODY HTML", body_html)
            print("VENDOR", vendor)
            print("PROUCT TYPE", product_type)
            print("STATUS", status)

            shopify_client = ShopifyClient()
            shopify_inst = shopify_client._shopify
            print("PRODUCT NEW ACCESS TOKEN", shopify_client.access_token)
            print("SHOPIFY INSTANCE", shopify_client._shopify)
            new_product = shopify_inst.Product()
            new_product.title = title
            # new_product.body_html = body_html
            # new_product.vendor = vendor
            # new_product.product_type = product_type
            # new_product.status = status
            # new_product.price = 19.99
            new_product.save()
            return render(request, 'products/product_form_success.html')
        else:
            # Handle form errors
            return render(request, 'products/product_create.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'products/product_create.html', {'form': form})
