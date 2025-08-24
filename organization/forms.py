from django import forms
from .models import OrganizationUnit


class OrganizationUnitForm(forms.ModelForm):
    class Meta:
        model = OrganizationUnit
        exclude = ('custom_id',)

    def __init__(self, *args, **kwargs):
        super(OrganizationUnitForm, self).__init__(*args, **kwargs)
        # Create indented labels
        units = OrganizationUnit.objects.all()

        def build_choices(units, parent=None, level=0):
            result = []
            for unit in units.filter(parent=parent).order_by('name'):
                prefix = '—' * level
                result.append((unit.id, f"{prefix} {unit.name}"))
                result += build_choices(units, parent=unit, level=level + 1)
            return result

        self.fields['parent'].queryset = units
        self.fields['parent'].label_from_instance = lambda obj: obj.name
        self.fields['parent'].choices = [('', '---------')] + build_choices(units)
