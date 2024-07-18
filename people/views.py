from django.shortcuts import render
from .models import Person

def home(request):
    return render(request, 'home.html')

def person_list(request):
    persons = Person.objects.all()
    return render(request, 'people/person_list.html', {'persons': persons})
