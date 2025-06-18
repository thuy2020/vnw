import json
import os
import django
from people.resume_parser import parse_resume_text

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vnw.settings')
django.setup()

from people.models import Person, PersonPosition

with open('gov_individuals.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

success, failed = 0, 0

for item in records:
    try:
        parsed = parse_resume_text(item.get('resume_text', ''))

        person, created = Person.objects.update_or_create(
            name=item.get('name'),
            defaults={
                'resume_url': item.get('resume_url'),
                'cabinet': item.get('cabinet'),
                'cabinet_url': item.get('cabinet_url'),
                'position': item.get('position'),
                'education': parsed.get('education'),
                'ethnicity': parsed.get('ethnicity'),
                'hometown': parsed.get('hometown'),
                'foreign_language': parsed.get('foreign_language'),
                'political_theory': parsed.get('political_theory'),
                'date_entered_party': parsed.get('date_entered_party'),
                'date_entered_party_official': parsed.get('date_entered_party_official'),
                'position_process': parsed.get('position_process'),
                'degree': parsed.get('degree'),
                'rank': parsed.get('rank'),
            }
        )

        # Clear previous positions
        PersonPosition.objects.filter(person=person).delete()

        # Add top-level positions
        for p in parsed.get('positions', []):
            PersonPosition.objects.create(person=person, title=p)

        # Add timeline positions
        for entry in parsed.get('position_history', []):
            PersonPosition.objects.create(
                person=person,
                title=entry.get('title'),
                start=entry.get('start'),
                end=entry.get('end')
            )

        success += 1

    except Exception as e:
        print(f"❌ Failed to import {item.get('name')}: {e}")
        failed += 1

print(f"\n✅ Successfully imported: {success}")
print(f"❌ Failed imports: {failed}")
