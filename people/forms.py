from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name',
                  'year_of_birth',
                  'hometown',
                  'current_workplace',
                  'current_workposition']