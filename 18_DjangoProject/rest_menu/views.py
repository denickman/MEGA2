from django.shortcuts import render
from django.views import generic
from .models import *

class Menu(generic.ListView):
    qeuryset = Item.objects.order_by('-date_created')
    template_name = 'index.html'






class MenuItem(generic.DetailView):
    model = Item
    template_name = 'menu_item_detail.html'
    
