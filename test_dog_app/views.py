from django.shortcuts import render
from .models import DogName, Entry
from rest_framework import viewsets
from .serializer import DogNameSerializer, EntrySerializer
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
    dog_name = DogName.objects.all()
    dog_bio = Entry.objects.all()

    content = {
        'dog_name': dog_name,
        'dog_bio': dog_bio
    }
    return render(request, 'authors_dog.html', content)

