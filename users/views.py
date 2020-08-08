from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages
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

