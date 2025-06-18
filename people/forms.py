from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'degree', 'rank',
                  'ethnicity', 'education', 'hometown',
                  'position', 'foreign_language', 'political_theory',
                  'date_entered_party', 'date_entered_party_official',
                  'cabinet', 'cabinet_url', 'resume_url']
