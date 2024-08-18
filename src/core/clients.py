# Built-in
from typing import List, Dict

# Django
from django.conf import settings

# 3rd Party
import shopify
from shopify import Session as ShopifySession


class NoLongerValidShopifyAccessToken(Exception):
    pass


class ShopifyClient:

    _shopify = None
    shopify_session = None
    auth_url = ""
    shop = None

    def __new__(cls):

        if not hasattr(cls, 'instance'):
            cls.instance = super(ShopifyClient, cls).__new__(cls)
        else:
            try:
                if hasattr(cls.instance, 'access_token') and cls.instance.access_token:
                    instance = cls.instance
                    access_token = instance.access_token
                    print("NEW PHASE ACCESS TOKEN", access_token)

                    _shopify = instance._shopify
                    if access_token and _shopify:
                        shopify_session = ShopifySession(
                            settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION,
                            access_token)
                        shopify.ShopifyResource.activate_session(shopify_session)
                        cls.instance._shopify = shopify
                        print("DONE SETTING NEW SHOPIFY INSTANCE")
            except Exception:
                raise NoLongerValidShopifyAccessToken("Access token no longer valid for Shopify")

        return cls.instance

    def __del__(self):
        print("Clearing Shopify Session")
        shopify.ShopifyResource.clear_session()

    def __init__(self):
        ShopifySession.setup(
            api_key=settings.SHOPIFY_API_CLIENT,
            secret=settings.SHOPIFY_API_SECRET
        )

    def init_auth(self, scopes: List[str] = [], redirect_uri: str = ""):
        shopify_session = ShopifySession(
            settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION)
        auth_url = shopify_session.create_permission_url(scopes, redirect_uri)
        return auth_url

    def activate_session(self, shopify_query_params: Dict[str, List[str]]):

        shopify_session = ShopifySession(
            settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION)
        access_token = shopify_session.request_token(shopify_query_params)
        self.access_token = access_token
        print("ACCESS TOKEN", access_token)

        shopify_session = ShopifySession(
            settings.SHOPIFY_STORE_URL, settings.SHOPIFY_API_VERSION,
            access_token)
        shopify.ShopifyResource.activate_session(shopify_session)

        # set shop instance
        self._shopify = shopify
