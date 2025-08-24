from django.urls import path
from .views import person_list, add_person, cabinet_list, cabinet_detail

urlpatterns = [
    path('', person_list, name='person_list'),
    path('add/', add_person, name='add_person'),
    path('cabinets/', cabinet_list, name='cabinet_list'),
    path('cabinets/<int:cabinet_id>/', cabinet_detail, name='cabinet_detail'),
]
