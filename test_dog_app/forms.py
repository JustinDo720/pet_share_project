from django import forms
from .models import DogName, Entry


class DogNameForm(forms.ModelForm):
    class Meta:
        model = DogName
        fields = ['name']
        labels = {'name': 'Dog name:'}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['bio_entry', 'dog_photo']
        labels = {'bio_entry': 'Dog\'s Biography', 'dog_photo': 'Dog\'s Photo'}
        widgets = {'bio_entry': forms.Textarea(attrs={'cols':100})}

