from django.shortcuts import render, redirect
from .forms import RegisterForm, ChangeUserNameForm, ChangeProfilePictureForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from test_dog_app.models import DogName, Entry, Profile
from django.http import Http404
# Create your views here.


def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} was successfully added.')
            new_user = form.save()
            login(request, new_user)
            return redirect('test_dog_app:index')

    return render(request, 'registration/register.html', {'form': form})  # registration/template.html is required!


@login_required
def user_private_profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    user_dogs = profile.dogname_set.all()

    if profile.user != request.user:
        raise Http404

    content = {'user_dogs' : user_dogs,}
    return render(request, 'user_private_profile.html', content)


@login_required
def user_profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    user_dogs = profile.dogname_set.filter(share=True)

    content = {
        'profile': profile,
        'user_dogs' : user_dogs,
    }
    return render(request, 'user_profile.html', content)


@login_required
def edit_user_profile(request, user_id):
    profile = Profile.objects.get(id=user_id)

    if request.method != 'POST':
        p_form = ChangeProfilePictureForm(instance=profile)
        u_form = ChangeUserNameForm(instance=request.user)
    else:
        p_form = ChangeProfilePictureForm(instance= profile,
                                          data= request.POST,
                                          files= request.FILES)
        u_form = ChangeUserNameForm(instance=request.user,
                                    data=request.POST)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()

            return redirect('users:user_private_profile', user_id= profile.id)

    context = {
        'p_form':p_form,
        'u_form':u_form,
        'profile': profile
    }

    return render(request, 'edit_user_profile.html', context)

