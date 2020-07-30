from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DogName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Entry(models.Model):
    dog_name = models.ForeignKey(DogName, on_delete=models.CASCADE)
    bio_entry = models.TextField()
    dog_photo = models.ImageField(default=None, upload_to='photo_img/', blank=True)
    date_entry = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bio_entry[:50]


