from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Dog Name', views.DogNameViewSet)
router.register('Biography', views.EntryViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('rest_api_info', include(router.urls), name='rest_api_info'),
    path('', views.index, name='index'),
    path('authors_dog', views.authors_dog, name='authors_dog')

]
