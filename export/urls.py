from django.urls import path
from . import views

urlpatterns = [
    path("download/organizations/", views.download_organizations_csv, name="download_organizations_csv"),
    path("download/people/", views.download_people_csv, name="download_people_csv"),
    path("download/positions/", views.download_positions_csv, name="download_positions_csv"),
    path("download/nodes/", views.download_nodes_csv, name="download_nodes_csv"),
    path("download/edges/", views.download_edges_csv, name="download_edges_csv"),
    path("download/network.json", views.download_network_json, name="download_network_json"),
]