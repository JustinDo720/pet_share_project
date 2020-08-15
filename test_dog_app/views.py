from django.shortcuts import render, redirect
from .models import DogName, Entry, Profile
from .serializer import DogNameSerializer, EntrySerializer, ProfileSerializer
from rest_framework import viewsets
from .forms import DogNameForm, EntryForm
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

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

    paginator = Paginator(dog_entries, 3)
    page_number = request.GET.get('page')

    dog_entries = paginator.get_page(page_number)

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
            new_dog_name.owner_profile = request.user.profile
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


def community_page(request):
    shareable_dogs = DogName.objects.filter(share=True).order_by('-shared_date')
    shareable_entries = Entry.objects.filter(share=True).order_by('-shared_date')

    paginator = Paginator(shareable_dogs, 3)    # Set a paginator with the items, number of items per page
    page_number = request.GET.get('page', 1)   # /?page=number NOTE: url must have trailing / to take parameters

    shareable_dogs = paginator.get_page(page_number)    # showcases each 3 or less dogs per page

    context = {'shareable_entries': shareable_entries, 'shareable_dogs':shareable_dogs}
    return render(request, 'community_page.html', context)


def full_dog_page(request, dog_id):
    dog_shared = DogName.objects.get(id=dog_id)
    dog_entries = dog_shared.entry_set.filter(share=True)

    paginator = Paginator(dog_entries, 3)
    page_number = request.GET.get('page')

    dog_entries = paginator.get_page(page_number)

    content = {
        'dog_shared': dog_shared,
        'dog_entries': dog_entries
    }

    return render(request, 'full_dog_page.html', content)


def share_dog(request, dog_id):
    dog_to_share = DogName.objects.get(id=dog_id)
    dog_info = dog_to_share.entry_set.filter(share=False).order_by('-date_entry')
    all_dog_entries = dog_to_share.entry_set.all()

    if request.method == 'POST':
        entry_to_share = request.POST.getlist('entry')
        if entry_to_share:  # If users checked any box then we run the for loop
            date_shared = timezone.now()
            dog_to_share.share = True
            dog_to_share.shared_date = date_shared
            dog_to_share.save()
            for entry in entry_to_share:
                change_entry_share = Entry.objects.get(id=entry)
                date_shared = timezone.now()
                change_entry_share.shared_date = date_shared
                change_entry_share.share = True
                change_entry_share.save()
        else:
            dog_to_share.share = False
            dog_to_share.save()
            for entry in dog_info:
                entry.share = False
                entry.save()

        return redirect('test_dog_app:community_page')

    paginator = Paginator(dog_info, 3)

    page_number = request.GET.get('page', 1)
    dog_info = paginator.get_page(page_number)

    content = {
        'dog_to_share':dog_to_share,
        'dog_info':dog_info,
        'all_dog_entries':all_dog_entries,
    }
    return render(request, 'share_dog.html',content)


@login_required
def community_profile(request):
    dog_name = DogName.objects.filter(owner=request.user.id, share=True).order_by('-shared_date')
    entries = Entry.objects.filter(share=True).order_by('-shared_date')
    all_user_dogs = DogName.objects.filter(owner=request.user.id)
    print(all_user_dogs)
    if request.method == 'POST':
        remove_entries = request.POST.getlist('entry')
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

    content= {
        'dog_name': dog_name,
        'entries': entries,
        'all_user_dogs': all_user_dogs
    }
    return render(request, 'community_profile.html', content)


def remove_entry(request, entry_id):
    entry_to_delete = Entry.objects.get(id=entry_id)
    entry_to_delete.delete()
    messages.warning(request, f'You have removed an entry from {entry_to_delete.dog_name}.')

    return redirect('test_dog_app:user_private_entries', dog_id= entry_to_delete.dog_name.id)


def remove_dog(request, dog_id):
    dog_to_delete = DogName.objects.get(id=dog_id)
    dog_to_delete.delete()
    messages.warning(request, f'You have removed {dog_to_delete} from your pets list.')

    return redirect('test_dog_app:user_entries')


def tutorial(request):
    return render(request, 'tutorial.html')
