from django.urls import path
from .views import person_list, add_person

urlpatterns = [
    path('', person_list, name='person_list'),
    path('add/', add_person, name='add_person'),
]
