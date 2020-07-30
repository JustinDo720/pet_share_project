from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

router.register('Dog\'s Name', views.DogNameViewSet)
router.register('Dog\'s Biography', views.EntryViewSet)

app_name = 'test_dog_app'

urlpatterns = [
    path('rest_auth/', include('rest_framework.urls')),
    path('dog_rest_api/',include(router.urls)),
    path('', views.index, name='index'),
    path('authors_dog', views.authors_dog, name='authors_dog'),
    path('user_entries/', views.user_entries, name= 'user_entries'),
    path('user_entries/<int:dog_id>/', views.user_private_entries, name= 'user_private_entries'),
    path('add_dog_name/', views.add_dog_name, name= 'add_dog_name'),
    path('write_about_dog/<int:dog_id>/', views.write_about_dog, name='write_about_dog'),
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)


