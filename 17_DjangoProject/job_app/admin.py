from django.contrib import admin
from .models import FormUser


class FormAdmin(admin.ModelAdmin):
    # field that will be represented in real form in web page
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('date', 'occupation')
    ordering = ('-first_name')
    readonly_fields = ('occupation')




admin.site.register(FormUser, FormAdmin) # \admin

# to create an admin you need to go in terminal - python manage.py createsuperuser