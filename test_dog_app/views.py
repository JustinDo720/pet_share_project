from django.shortcuts import render, redirect
from .models import DogName, Entry
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
    dog_name = DogName.objects.all()
    dog_bio = Entry.objects.all()

    content = {
        'dog_name': dog_name,
        'dog_bio': dog_bio
    }
    return render(request, 'user_entries.html', content)


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

