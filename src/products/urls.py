from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.product_list, name='list'),
    path('verify', views.verify, name='verify'),
    path('redirected', views.redirected, name='redirected'),
    path('create_or_edit', views.product_create_or_edit, name='create_or_edit'),
]
