from django.shortcuts import render, redirect
from .models import Person
from .forms import PersonForm

def home(request):
    return render(request, 'home.html')

def person_list(request):
    persons = Person.objects.all()
    return render(request, 'people/person_list.html', {'persons': persons})


def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'people/add_person.html', {'form': form})
