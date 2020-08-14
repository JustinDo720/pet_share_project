from django import forms
from .models import DogName, Entry


class DogNameForm(forms.ModelForm):
    class Meta:
        model = DogName
        fields = ['name']
        labels = {'name': 'Pet\'s name:'}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['bio_entry', 'dog_photo']
        labels = {'bio_entry': 'Pet\'s Biography', 'dog_photo': 'Pet\'s Photo'}
        widgets = {'bio_entry': forms.Textarea(attrs={'cols':100})}

