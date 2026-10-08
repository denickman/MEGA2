from django.urls import path
from . import views

urlpatterns = [
    path('', views.Menu.as_view(), name='home'),
]
