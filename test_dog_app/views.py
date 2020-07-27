from django.shortcuts import render
from .models import DogName, Entry
from .serializer import DogNameSerializer, EntrySerializer
from rest_framework import viewsets

# Create your views here.


class DogNameViewSet(viewsets.ModelViewSet):
    queryset = DogName.objects.all()
    serializer_class = DogNameSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


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


def write_about_dog(request):
    entry_ = Entry.objects.create()

    content = {
    'entry_': entry_
    }
    return render(request, 'write_about_dog.html',content)
