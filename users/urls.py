from django.urls import path,include
from . import views


app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')), # This adds all that urls that deal with login and out
    path('register/', views.register, name='register'),
]
