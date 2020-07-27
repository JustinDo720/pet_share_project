from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors_dog', views.authors_dog, name='authors_dog'),
    path('user_entries', views.user_entries, name = 'user_entries')

]
