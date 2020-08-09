from django.shortcuts import render, redirect
from .models import DogName, Entry, Profile
from .serializer import DogNameSerializer, EntrySerializer, ProfileSerializer
from rest_framework import viewsets
from .forms import DogNameForm, EntryForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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


@login_required
def user_entries(request):
    dogs = DogName.objects.filter(owner=request.user.id)   # With this filter, the owners only get to see their dog
    content = {
        'dogs': dogs
    }
    return render(request, 'user_entries.html', content)


@login_required
def user_private_entries(request, dog_id):
    dog = DogName.objects.get(id=dog_id)
    dog_entries = dog.entry_set.order_by('-date_entry')

    if dog.owner != request.user:
        raise Http404

    content = {
        'dog': dog,
        'dog_entries': dog_entries
    }
    return render(request, 'user_private_entries.html', content)


@login_required
def add_dog_name(request):

    if request.method != 'POST':
        form = DogNameForm()
    else:
        form = DogNameForm(data=request.POST)
        if form.is_valid():
            new_dog_name = form.save(commit=False)
            new_dog_name.owner = request.user   # This puts the new dog under the requested user
            new_dog_name.save()
            return redirect('test_dog_app:user_entries')

    content = {'form': form}
    return render(request, 'add_dog_name.html', content)


@login_required
def write_about_dog(request, dog_id):
    dog = DogName.objects.get(id=dog_id)

    if dog.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST, files= request.FILES)
        if form.is_valid():
            new_bio = form.save(commit=False)
            new_bio.dog_name = dog      # This refers to which dog the bio/form belongs to
            # print(new_bio.dog_photo)
            new_bio.save()
            return redirect('test_dog_app:user_private_entries', dog_id=dog_id)

    content = {'form': form, 'dog': dog}
    return render(request, 'write_about_dog.html', content)


@login_required
def edit_dog_name(request, dog_id):
    dog_name = DogName.objects.get(id=dog_id)

    if dog_name.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = DogNameForm(instance=dog_name)
    else:
        form = DogNameForm(instance=dog_name, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('test_dog_app:user_entries')

    return render(request, 'edit_dog_name.html', {'form':form, 'dog_name': dog_name})


@login_required
def edit_dog_bio(request, entry_bio_id):
    dog_entries = Entry.objects.get(id= entry_bio_id)
    dogs = dog_entries.dog_name

    if dogs.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Fetching original entry
        form = EntryForm(instance=dog_entries)
    else:
        # Allow the user to POST their edits
        form = EntryForm(instance=dog_entries, data= request.POST, files= request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect('test_dog_app:user_private_entries', dog_id=dogs.id)

    content = {
        'form': form,
        'dogs': dogs,
        'dog_entries': dog_entries
    }
    return render(request, 'edit_dog_bio.html', content)


def all_entries(request):
    shareable_dogs = DogName.objects.filter(share=True)
    shareable_entries = Entry.objects.filter(share=True)
    context = {'shareable_entries': shareable_entries, 'shareable_dogs':shareable_dogs}
    return render(request, 'all_entries.html', context)


def share_dog(request, dog_id):
    dog_to_share = DogName.objects.get(id=dog_id)
    dog_info = dog_to_share.entry_set.filter(share=False)
    all_dog_entries = dog_to_share.entry_set.all()

    if request.method == 'POST':
        entry_to_share = request.POST.getlist('entry')
        print(entry_to_share)
        if entry_to_share:  # If users checked any box then we run the for loop
            dog_to_share.share = True
            dog_to_share.save()
            for entry in entry_to_share:
                change_entry_share = Entry.objects.get(id=entry)
                change_entry_share.share = True
                change_entry_share.save()
        else:
            dog_to_share.share = False
            dog_to_share.save()
            for entry in dog_info:
                entry.share = False
                entry.save()

        return redirect('test_dog_app:all_entries')

    content = {
        'dog_to_share':dog_to_share,
        'dog_info':dog_info,
        'all_dog_entries':all_dog_entries,
    }
    return render(request, 'share_dog.html',content)


def community_profile(request):
    dog_name = DogName.objects.filter(owner=request.user.id, share=True)
    entries = Entry.objects.filter(share=True)

    if request.method == 'POST':
        remove_entries = request.POST.getlist('entry')
        print(remove_entries)
        if remove_entries:
            for entry in remove_entries:
                entry_to_remove = Entry.objects.get(id=entry)
                entry_to_remove.share = False
                entry_to_remove.save()
        for dog in dog_name:
            specific_entries = [entry for entry in entries if entry.dog_name == dog]
            if specific_entries:
                dog.share = True
                dog.save()
            else:
                dog.share = False
                dog.save()
        return redirect('test_dog_app:community_profile')

    return render(request, 'community_profile.html', {'dog_name':dog_name, 'entries':entries})

