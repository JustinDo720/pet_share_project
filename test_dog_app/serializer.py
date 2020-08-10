from rest_framework import serializers
from .models import DogName, Entry, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_photo']


class DogNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogName
        fields = [
            'id', 'owner','name', 'share'
        ]


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = [
            'id', 'dog_name', 'share','bio_entry','dog_photo','date_entry', 'shared_date'
        ]


