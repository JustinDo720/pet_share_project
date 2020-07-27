from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('Dog\'s Name', views.DogNameViewSet)
router.register('Dog\'s Biography', views.EntryViewSet)

urlpatterns = [
    path('rest_auth/', include('rest_framework.urls')),
    path('dog_rest_api/',include(router.urls)),
    path('', views.index, name='index'),
    path('authors_dog', views.authors_dog, name='authors_dog'),
    path('user_entries', views.user_entries, name = 'user_entries')

]
