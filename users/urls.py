from django.urls import path,include
from . import views


app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')), # This adds all that urls that deal with login and out
    path('register/', views.register, name='register'),
    path('user_private_profile/<int:user_id>/', views.user_private_profile, name='user_private_profile'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('edit_user_profile/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
]
