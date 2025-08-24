from django.shortcuts import render, redirect, get_object_or_404
from .models import Person, Cabinet
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

# views.py
def cabinet_list(request):
    cabinets = Cabinet.objects.all()
    return render(request, "people/cabinet_list.html", {"cabinets": cabinets})


def cabinet_detail(request, cabinet_id):
    cabinet = get_object_or_404(Cabinet, id=cabinet_id)
    members = cabinet.members.all()
    return render(request, "people/cabinet_detail.html",
                  {"cabinet": cabinet, "members": members})