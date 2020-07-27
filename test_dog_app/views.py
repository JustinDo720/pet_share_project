from django.shortcuts import render
from .models import DogName, Entry
# Create your views here.


def index(request):
    return render(request, 'index.html')


def authors_dog(request):
    return render(request, 'authors_dog.html')


def user_entries(request):
    dog_name = DogName.objects.all()
    dog_bio = Entry.objects.all()

    content = {
        'dog_name': dog_name,
        'dog_bio': dog_bio
    }
    return render(request, 'user_entries.html',content)