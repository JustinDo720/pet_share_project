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
    user_dogs = DogName.objects.all()  # This must be the same as user_private_entries

    content = {
        'user_dogs': user_dogs
    }
    return render(request, 'user_entries.html', content)


def user_private_entries(request, user_entry_id):
    user_dog = DogName.objects.get(id=user_entry_id)
    user_dog_entries = user_dog.entry_set.all()

    content = {
        'user_dog': user_dog,
        'user_dog_entries': user_dog_entries
    }
    return render(request, 'user_private_entries.html', content)


def add_dog_name(request):
    if request.method != 'POST':
        form = DogNameForm()
    else:
        form = DogNameForm(data=request.POST)
        if form.is_valid:
            new_dog_name = form.save(commit=False)
            new_dog_name.save()
            return redirect('test_dog_app:user_entries')

    content = {'form': form}
    return render(request, 'add_dog_name.html', content)


def write_about_dog(request):
    pass

