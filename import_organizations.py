import pandas as pd
from datetime import datetime
import os
import django

from core.normalization import normalize_vietnamese_name
from core.utils import get_or_create_existing_organization
from django.db.models.functions import Lower

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vnw.settings")
django.setup()

from organizations.models import Organization, OrganizationType

def parse_date(date_str):
    if pd.isna(date_str):
        return None
    try:
        return pd.to_datetime(date_str).date()
    except Exception:
        return None

def import_organizations_from_excel(filepath):
    df = pd.read_excel(filepath)

    pending = df.to_dict(orient="records")
    created_names = set()
    processed_names = set()

    # Build map of normalized org names to org objects for deduplication
    existing_orgs = {normalize_vietnamese_name(org.name): org for org in Organization.objects.all()}

    for _ in range(5):  # try up to 5 passes
        remaining = []
        for row in pending:
            name = row.get("name")
            if not name:
                continue

            parent = None
            parent_name_raw = row.get("parent_name")
            if pd.notna(parent_name_raw) and str(parent_name_raw).strip():
                parent_name = str(parent_name_raw).strip()
                normalized_parent_name = normalize_vietnamese_name(parent_name)
                parent = existing_orgs.get(normalized_parent_name)
                if not parent:
                    remaining.append(row)
                    continue

            org_type = None
            if pd.notna(row.get("type")):
                org_type, _ = OrganizationType.objects.get_or_create(name=row["type"].strip())

            normalized_name = normalize_vietnamese_name(name)
            org = existing_orgs.get(normalized_name)

            org = get_or_create_existing_organization(
                name=name.strip(),
                abbreviation=row.get("abbreviation"),
                name_en=row.get("name_en"),
                level=row.get("level"),
                org_type=org_type,
                parent=parent,
                function=row.get("function"),
                start_date=parse_date(row.get("start_date")),
                end_date=parse_date(row.get("end_date")),
                color_code=row.get("color_code"),
                description=row.get("description"),
            )
            existing_orgs[normalized_name] = org
            print(f"✅ Saved: {org.name}")

            created_names.add(org.name)
            processed_names.add(org.name)

            # Handle equivalent orgs
            if pd.notna(row.get("equivalent_names")):
                eq_names = [n.strip() for n in row["equivalent_names"].split(",")]
                for eq_name in eq_names:
                    eq_name_norm = normalize_vietnamese_name(eq_name)
                    eq_org = existing_orgs.get(eq_name_norm)
                    if not eq_org:
                        eq_org = Organization.objects.create(name=eq_name)
                        existing_orgs[eq_name_norm] = eq_org
                    org.equivalents.add(eq_org)

        if not remaining:
            break
        pending = remaining  # Retry rows with unresolved parents

    unresolved = [row for row in pending if row.get("name") not in processed_names]
    if unresolved:
        print("\n⚠️ The following rows could not be processed due to missing parents:")
        for row in unresolved:
            print(f"❌ {row.get('name')} (missing parent: {row.get('parent_name')})")

if __name__ == "__main__":
    import_organizations_from_excel("organizations.xlsx")