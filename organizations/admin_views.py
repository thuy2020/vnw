from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from organizations.models import Organization
from organizations.utils import merge_organizations



class MergeOrganizationsForm(forms.Form):
    primary = forms.ModelChoiceField(queryset=Organization.objects.all(), label="Primary Organization (Keep)")
    duplicate = forms.ModelChoiceField(queryset=Organization.objects.all(),
                                       label="Duplicate Organization (Merge & Delete)")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("primary") == cleaned_data.get("duplicate"):
            raise forms.ValidationError("You must select two different organizations.")
        return cleaned_data


def merge_organizations_view(request):
    if request.method == "POST":
        form = MergeOrganizationsForm(request.POST)
        if form.is_valid():
            primary = form.cleaned_data["primary"]
            duplicate = form.cleaned_data["duplicate"]

            # Use existing logic
            merge_organizations(duplicate, primary) # delete dup, keep primary

            messages.success(request, f"Merged '{duplicate}' into '{primary}' successfully.")
            return redirect("/admin/organizations/organization/")
    else:
        form = MergeOrganizationsForm()

    return render(request, "admin/merge_organizations.html", {"form": form})