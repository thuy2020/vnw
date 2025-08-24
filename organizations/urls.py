
from django.urls import path
from .views import (
    organization_list,
    add_organization_unit,
    edit_organization_unit,
    import_organization_units,
    organization_tree_view,
    inline_edit_organization_unit,
    view_relationships,
)

urlpatterns = [
    path('', organization_list, name='organization_list'),
    path('add/', add_organization_unit, name='add_organization_unit'),
    path('edit/<int:unit_id>/', edit_organization_unit, name='edit_organization_unit'),
    path('import/', import_organization_units, name='import_organization_units'),
    path('tree/', organization_tree_view, name='organization_tree_view'),
    path('inline-edit/<int:unit_id>/', inline_edit_organization_unit, name='inline_edit_organization_unit'),
    path('relationships/<int:unit_id>/', view_relationships, name='view_relationships'),
]
