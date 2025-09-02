
def get_or_create_existing_organization(name, **defaults):
    from organizations.models import Organization
    from core.normalization import normalize_vietnamese_name

    if not name:
        return None

    normalized_name = normalize_vietnamese_name(name)
    existing = Organization.objects.filter(normalized_name_ascii__iexact=normalized_name).first()

    return existing or Organization.objects.create(name=name, name_ascii=normalized_name, **defaults)