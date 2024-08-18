# Built-in
from urllib.parse import urlencode

# Django
from django.shortcuts import render, redirect

# Local
from core import ShopifyClient

from .forms import ProductForm


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
