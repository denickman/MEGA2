from django.contrib.auth.models import User
from django.db import models

MEAL_TYPE = ( # first letter word - small for frontend part, second word letter - Big
    ('standard', 'Standard'),
    ('drink', 'Drink'),
    ('main_dishes', 'Main Dishes'),
    ('desserts', 'Desserts'),
)

STATUS = (
    (0, 'unavailable'),
    (1, 'available'),
)


class Item(models.Model):
    meal = models.CharField(max_length=1000, unique=True)
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    meal_type = models.CharField(max_length=200, choices=MEAL_TYPE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # user is also a table in data base
    status = models.IntegerField(choices=STATUS, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.meal
