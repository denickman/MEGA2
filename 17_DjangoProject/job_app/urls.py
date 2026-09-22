from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), # the home page should be connected to this function 
]