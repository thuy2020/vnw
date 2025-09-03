import json
import os
from django.http import FileResponse, JsonResponse
from django.conf import settings
from organizations.models import Organization
import csv
from people.models import Person, PersonPosition

EXPORT_DIR = os.path.join(settings.BASE_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

def download_organizations_csv(request):
    file_path = os.path.join(EXPORT_DIR, "organizations.csv")

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Custom ID", "Name", "Type", "Parent"])

        for org in Organization.objects.select_related('type', 'parent').all():
            writer.writerow([
                org.id,
                org.custom_id,
                org.name,
                org.type.name if org.type else "",
                org.parent.name if org.parent else ""
            ])

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='organizations.csv')



def download_people_csv(request):
    file_path = os.path.join(EXPORT_DIR, "people.csv")

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Custom ID", "Name", "Date of Birth", "Hometown", "Current Position"])

        for p in Person.objects.all():
            writer.writerow([
                p.id,
                p.custom_id,
                p.name,
                p.date_of_birth,
                p.hometown_province,
                p.position,

            ])

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='people.csv')


def download_positions_csv(request):
    file_path = os.path.join(EXPORT_DIR, "positions.csv")

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Person", "Organization", "Title", "Start", "End"])

        for pos in PersonPosition.objects.select_related("person", "organization").all():
            writer.writerow([
                pos.id,
                pos.person.name if pos.person else "",
                pos.organization.name if pos.organization else "",
                pos.title,
                pos.start,
                pos.end,
            ])

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='positions.csv')


def download_nodes_csv(request):
    file_path = os.path.join(EXPORT_DIR, "nodes.csv")
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Label", "Type"])
        for org in Organization.objects.all():
            writer.writerow([f"org_{org.id}", org.name, "organization"])
        for person in Person.objects.all():
            writer.writerow([f"person_{person.id}", person.name, "person"])
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='nodes.csv')


def download_edges_csv(request):
    file_path = os.path.join(EXPORT_DIR, "edges.csv")
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Relationship", "Title", "Start", "End"])
        for pos in PersonPosition.objects.select_related("person", "organization"):
            writer.writerow([
                f"person_{pos.person.id}" if pos.person else "",
                f"org_{pos.organization.id}" if pos.organization else "",
                "holds_position",
                pos.title,
                pos.start,
                pos.end
            ])
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='edges.csv')


def download_network_json(request):
    file_path = os.path.join(EXPORT_DIR, "network.json")

    nodes = []
    for org in Organization.objects.all():
        nodes.append({
            "id": f"org_{org.id}",
            "label": org.name,
            "type": "organization"
        })
    for person in Person.objects.all():
        nodes.append({
            "id": f"person_{person.id}",
            "label": person.name,
            "type": "person"
        })

    edges = []
    for pos in PersonPosition.objects.select_related("person", "organization"):
        if pos.person and pos.organization:
            edges.append({
                "source": f"person_{pos.person.id}",
                "target": f"org_{pos.organization.id}",
                "label": pos.title,
                "type": "holds_position",
                "start": str(pos.start) if pos.start else None,
                "end": str(pos.end) if pos.end else None
            })

# Write to file
    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "edges": edges}, f, ensure_ascii=False, indent=2)

    # Serve as file download
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename="network.json")