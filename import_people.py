import json
import os
import django
from django.contrib import admin

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vnw.settings')
django.setup()

from people.resume_parser import parse_resume_text
from people.models import Person, PersonPosition, Cabinet
from organizations.models import Organization


def safe_parse_resume(resume_text):
    try:
        parsed = parse_resume_text(resume_text or "")
        # Ensure position_history is always a list
        parsed["position_history"] = parsed.get("position_history", [])
        return parsed
    except Exception as e:
        print(f"⚠️ Resume parsing failed: {e}")
        return {"position_history": []}

def truncate(value, length):
    if not value:
        return None
    return str(value).strip()[:length]

def create_or_update_person(item):
    parsed = safe_parse_resume(item.get("resume_text", ""))

    # Fall back to original item fields if parsed field is missing
    parsed["hometown"] = parsed.get("hometown") or item.get("hometown")
    parsed["education"] = parsed.get("education") or item.get("education")
    parsed["ethnicity"] = parsed.get("ethnicity") or item.get("ethnicity")
    parsed["position"] = parsed.get("position") or item.get("position")
    parsed["position_process"] = parsed.get("position_process") or item.get("position_process")
    parsed["position_history"] = parsed.get("position_history") or item.get("position_history", [])
    parsed["gender"] = parsed.get("gender") or item.get("gender")



    if not parsed["position_history"]:
        parsed_fallback = safe_parse_resume(item.get("resume_text", ""))
        parsed["position_history"] = parsed_fallback.get("position_history", [])

    name = truncate(item.get("name"), 100) or "Unknown"
    resume_url = item.get("resume_url") or item.get("url") or f"unknown-url://{name.replace(' ', '_')}"
    hometown = truncate(parsed.get("hometown"), 150) or "Unknown"
    date_of_birth = parsed.get("date_of_birth")

    person, created = Person.objects.update_or_create(
        name=name,
        hometown=hometown,
        date_of_birth=date_of_birth,
        defaults={
            "position": truncate(item.get("position"), 100),
            "education": truncate(parsed.get("education"), 100),
            "ethnicity": truncate(parsed.get("ethnicity"), 100),
            "foreign_language": truncate(parsed.get("foreign_language"), 100),
            "political_theory": truncate(parsed.get("political_theory"), 100),
            "date_entered_party": parsed.get("date_entered_party"),
            "date_entered_party_official": parsed.get("date_entered_party_official"),
            "position_process": truncate(parsed.get("position_process"), 2000),
            "degree": truncate(parsed.get("degree"), 100),
            "rank": truncate(parsed.get("rank"), 100),
            "resume_text": item.get("resume_text"),
            "gender": parsed.get("gender"),
            "hometown_province": truncate(parsed.get("hometown_province"), 100),
        }


    )

    # Associate with cabinet
    cabinet_name = truncate(item.get("cabinet"), 300)
    cabinet_url = item.get("cabinet_url")
    if cabinet_name:
        cabinet, _ = Cabinet.objects.get_or_create(name=cabinet_name, defaults={"url": cabinet_url})
        person.cabinets.add(cabinet)

    # Clear previous positions
    PersonPosition.objects.filter(person=person).delete()

    # Add top-level positions
    for p in parsed.get("positions", []):
        if p:
            PersonPosition.objects.create(person=person, title=truncate(p, 255))

    # Add timeline positions with debug logging
    position_history = parsed.get("position_history", [])
    if not position_history:
        print(f"⚠️ No position history found for {name}")
    else:
        print(f"Parsed {len(position_history)} positions for {name}")
        for entry in position_history:
            print("  ->", entry)
            if entry.get("title"):
                org_name = entry.get("organizations")
                organization = None
                if org_name:
                    organization, _ = Organization.objects.get_or_create(name=org_name.strip())

                PersonPosition.objects.create(
                    person=person,
                    title=truncate(entry.get("title"), 1000),
                    start=entry.get("start"),
                    end=entry.get("end"),
                    organization=organization
                )
    return created

if __name__ == "__main__":
    with open("clean_individuals.json", "r", encoding="utf-8") as f:
        records = json.load(f)

#Delete all existing entries
   # Person.objects.all().delete()
   # Cabinet.objects.all().delete()

    success, failed, skipped = 0, 0, 0

    for item in records:
        try:
            created = create_or_update_person(item)
            success += 1
        except Exception as e:
            print(f"❌ Failed to import {item.get('name')}: {e}")
            failed += 1

    print(f"\n✅ Successfully imported: {success}")
    print(f"❌ Failed imports: {failed}")
