from django.db import models

# Create your models here.


class DogName(models.Model):
    name = models.CharField(max_length=70)
    date_entry = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    dog_name = models.ForeignKey('DogName', on_delete=models.CASCADE)
    bio_entry = models.CharField(max_length=500)

    def __str__(self):
        return self.bio_entry[:50]


