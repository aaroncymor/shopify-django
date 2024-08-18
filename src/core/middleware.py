# Built-in

# Django
from django.shortcuts import redirect

# 3rd party
from .clients import ShopifyClient


class ShopifyAccessTokenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        func_name = view_func.__name__
        print("FNAME", func_name)

        EXCLUDE_REDIRECT = ['verify', 'redirected']

        shopify_client = ShopifyClient()
        if not hasattr(shopify_client, 'access_token') and func_name not in EXCLUDE_REDIRECT:
            if func_name == "product_list":
                request.session['goto'] = 'list_product'
            elif func_name == "product_create_or_edit":
                request.session['goto'] = 'create_or_edit_product'

            return redirect('core:verify')  # Assuming 'product:verify' is your URL name
