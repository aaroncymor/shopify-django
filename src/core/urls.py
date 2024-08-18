from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('verify', views.verify, name='verify'),
    path('redirected', views.redirected, name='redirected'),
]
