"""following code registers the Game Record model with the Django admin site"""
"""written by Dylan, with aid in Django DB page doc"""
from django.contrib import admin

from .models import GameRecord

admin.site.register(GameRecord)

"""when running I used python manage.py migrate and then python manage.py runserver in the backend terminal"""
"""as noted by Django documentation and research it is so everyone can have their own local db and run migrations locally"""