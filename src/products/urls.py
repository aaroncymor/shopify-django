from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('redirected', views.redirected, name='redirected'),
]
