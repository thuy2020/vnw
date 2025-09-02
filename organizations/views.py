from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Organization
from .forms import OrganizationForm
import pandas as pd
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from core.utils import get_or_create_existing_organization

def organization_list(request):
    units = Organization.objects.all().order_by('type','name')
    return render(request, "organizations/organization_list.html", {'units':units})


def add_organization_unit(request):
    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organization_list')

    else:
            form = OrganizationForm()
    return render(request, "organizations/add_organization_unit.html",
                  {'form':form})

def edit_organization_unit(request, unit_id):
    unit = get_object_or_404(Organization, id=unit_id)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm(instance=unit)
    return render(request, 'organizations/edit_organization_unit.html', {'form': form, 'unit': unit})

def import_organization_units(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            for _, row in df.iterrows():
                name = row.get("name")
                if not name:
                    continue

                org = get_or_create_existing_organization(
                    name=name,
                    type=row.get("type"),
                    description=row.get("description"),
                    date_started=row.get("date_started"),
                    date_ended=row.get("date_ended")
                )
            messages.success(request, "Import completed successfully.")
        except Exception as e:
            messages.error(request, f"Import failed: {e}")
        return redirect('organization_list')
    return render(request, 'organizations/import_organization_unit.html')


# def organization_tree_view(request):
#     units = Organization.objects.all()
#     return render(request, 'organizations/organization_tree.html', {'units': units})


def inline_edit_organization_unit(request, unit_id):
    # Placeholder for inline editing logic
    unit = get_object_or_404(Organization, id=unit_id)
    return render(request, 'organizations/inline_edit_organization_unit.html', {'unit': unit})


def view_relationships(request, unit_id):
    unit = get_object_or_404(Organization, id=unit_id)
    children = unit.children.all()
    equivalents = unit.equivalents.all()
    return render(request, 'organizations/view_relationships.html', {
        'unit': unit,
        'children': children,
        'equivalents': equivalents
    })
def organization_chart(request):

    orgs = Organization.objects.select_related('parent', 'type').all()
    chart_data = []

    for org in orgs:
        level = org.level or ''
        if level == "central":
            color = 'red'
        elif level == "provincial":
            color = 'blue'
        else:
            color = 'gray'

        chart_data.append({
            'name': org.name,
            'parent': org.parent.name if org.parent else '',
            'type': org.type.name if org.type else '',
            'level': org.level if org.level else '',
            'id': org.id,
        })

    return render(request, 'organizations/org_chart.html', {
        'chart_data': chart_data
    })