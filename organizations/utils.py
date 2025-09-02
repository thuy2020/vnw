

from organizations.models import Organization
from people.models import PersonPosition
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def merge_organizations(source_org, target_org, dry_run=False):
    """
    Merges source_org into target_org:
    - Moves all PersonPosition references to target_org
    - Merges related children, related parents, and notes
    - Deletes source_org unless dry_run=True
    """
    log = []

    # Move all person positions
    positions = PersonPosition.objects.filter(organization=source_org)
    for pos in positions:
        log.append(f"Moved PersonPosition: {pos.person.name} ({pos.title}) from {source_org} to {target_org}")
        if not dry_run:
            pos.organization = target_org
            pos.save()

    # Merge related parents
    for parent in source_org.related_parents.exclude(id=target_org.id):
        if parent not in target_org.related_parents.all():
            log.append(f"Added related parent: {parent.name}")
            if not dry_run:
                target_org.related_parents.add(parent)

    # Merge related children
    for child in source_org.related_children.exclude(id=target_org.id):
        if child not in target_org.related_children.all():
            log.append(f"Added related child: {child.name}")
            if not dry_run:
                target_org.related_children.add(child)

    # Append notes
    if source_org.notes:
        log.append(f"Appended notes: {source_org.notes}")
        if not dry_run:
            if target_org.notes:
                target_org.notes += f"\n[Merged from {source_org.name}]: {source_org.notes}"
            else:
                target_org.notes = f"[Merged from {source_org.name}]: {source_org.notes}"
            target_org.save()

    # Delete source
    if not dry_run:
        log.append(f"Deleted source organization: {source_org}")
        source_org.delete()
    else:
        log.append(f"Dry run: did not delete source organization {source_org}")

    for line in log:
        logger.info(line)

    return log