# clean_duplicates.py
import django
import os
from collections import defaultdict
from core.normalization import normalize_vietnamese_name

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vnw.settings")
django.setup()

from organizations.models import Organization

def clean_duplicate_organizations():
    orgs = Organization.objects.all()
    groups = defaultdict(list)

    for org in orgs:
        norm_name = normalize_vietnamese_name(org.name)
        groups[norm_name].append(org)

    for norm_name, org_list in groups.items():
        if len(org_list) <= 1:
            continue  # No duplicates

        canonical = org_list[0]
        duplicates = org_list[1:]

        print(f"\n🧹 Merging duplicates for: {canonical.name}")

        for dup in duplicates:
            # Update parent references
            Organization.objects.filter(parent=dup).update(parent=canonical)

            # Update equivalents (many-to-many)
            for eq in dup.equivalents.all():
                canonical.equivalents.add(eq)

            # Add canonical to equivalents of others pointing to dup
            for o in Organization.objects.filter(equivalents=dup):
                o.equivalents.remove(dup)
                o.equivalents.add(canonical)

            # Transfer any reverse references (like in PersonPosition)
            # Add similar update lines here if needed

            # Finally, delete the duplicate
            print(f"❌ Deleting duplicate: {dup.name} (ID: {dup.id})")
            dup.delete()

    print("\n✅ Done cleaning duplicates.")

if __name__ == "__main__":
    clean_duplicate_organizations()