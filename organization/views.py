from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import OrganizationUnit
from .forms import OrganizationUnitForm

def organization_list(request):
    units = OrganizationUnit.objects.all().order_by('type','name')
    return render(request, "organization/organization_list.html", {'units':units})


def add_organization_unit(request):
    if request.method == "POST":
        form = OrganizationUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organization_list')

    else:
            form = OrganizationUnitForm()
    return render(request, "organization/add_organization_unit.html",
                      {'form':form})

def edit_organization_unit(request, unit_id):
    unit = get_object_or_404(OrganizationUnit, id=unit_id)
    if request.method == 'POST':
        form = OrganizationUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('organization_list')
    else:
        form = OrganizationUnitForm(instance=unit)
    return render(request, 'organization/edit_organization_unit.html', {'form': form, 'unit': unit})
