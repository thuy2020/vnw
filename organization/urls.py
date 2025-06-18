from django.urls import path
from . import views

urlpatterns = [
    path('', views.organization_list, name='organization_list'),  # ✅ This line is required
    path('add/', views.add_organization_unit, name='add_organization_unit'),
    path('edit/<int:unit_id>/', views.edit_organization_unit, name='edit_organization_unit'),
]
