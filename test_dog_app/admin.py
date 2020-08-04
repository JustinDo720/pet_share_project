from django.contrib import admin
from .models import DogName, Entry

# Register your models here.

admin.site.register(DogName)     # Registering the ability to enter Dog names
admin.site.register(Entry)      # Entering Bio for the dog
