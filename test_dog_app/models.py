from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_photo = models.ImageField(upload_to='user_photo/', default='default.png')

    def __str__(self):
        return self.user.username


class DogName(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    share = models.BooleanField(default=False)
    shared_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=False)

    def __str__(self):
        return self.name


class Entry(models.Model):
    dog_name = models.ForeignKey(DogName, on_delete=models.CASCADE, null=False)
    bio_entry = models.TextField()
    dog_photo = models.ImageField(default=None, upload_to='photo_img/', blank=True)
    share = models.BooleanField(default=False)
    date_entry = models.DateTimeField(auto_now_add=True)
    shared_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=False)

    def __str__(self):
        return f'{self.bio_entry[:50]}...'



