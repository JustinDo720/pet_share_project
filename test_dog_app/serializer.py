from rest_framework import serializers
from .models import DogName, Entry


class DogNameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DogName
        fields = [
            'id', 'name', 'date_entry'
            ]


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = [
            'id', 'dog_name', 'bio_entry'
            ]