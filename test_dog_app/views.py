from django.shortcuts import render, redirect
from .models import DogName, Entry, User
from .serializer import DogNameSerializer, EntrySerializer
from rest_framework import viewsets
from .forms import DogNameForm, EntryForm


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
    dogs = DogName.objects.all()  # This must be the same as user_private_entries

    content = {
        'dogs': dogs
    }
    return render(request, 'user_entries.html', content)


def user_private_entries(request, dog_id):
    dog = DogName.objects.get(id=dog_id)
    dog_entries = dog.entry_set.all()

    content = {
        'dog': dog,
        'dog_entries': dog_entries
    }
    return render(request, 'user_private_entries.html', content)


def add_dog_name(request):
    if request.method != 'POST':
        form = DogNameForm()
    else:
        form = DogNameForm(data=request.POST)
        if form.is_valid():
            new_dog_name = form.save(commit=False)
            new_dog_name.save()
            return redirect('test_dog_app:user_entries')

    content = {'form': form}
    return render(request, 'add_dog_name.html', content)


def write_about_dog(request, dog_id):
    dog = DogName.objects.get(id=dog_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_bio = form.save(commit=False)
            new_bio.dog_name = dog      # This refers to which dog the bio/form belongs to
            new_bio.save()
            return redirect('test_dog_app:user_private_entries', dog_id=dog_id)

    content = {'form': form, 'dog': dog}
    return render(request, 'write_about_dog.html', content)

