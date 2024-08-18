from django.urls import path
from . import views

urlpatterns = [
    path('verify', views.index, name='index'),
    path('redirected', views.redirected, name='redirected'),
    path('new', views.product_form_view, name='product_form'),
]
