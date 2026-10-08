from django.shortcuts import render
from django.views import generic
from .models import *

class Menu(generic.ListView):
    queryset = Item.objects.order_by('-date_created')   # опечатку исправили
    template_name = 'index.html'
    context_object_name = 'items'   # опционально: имя переменной в шаблоне (по умолчанию object_list)

# в шаблоне:
# {% for item in items %}
#     <li>{{ item.meal }} — {{ item.price }}</li>
# {% endfor %}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # берём то, что уже собрал ListView
        context['meals'] = 'Pizza'  # добавляем своё
        return context






class MenuItem(generic.DetailView):
    model = Item
    template_name = 'menu_item_detail.html'

