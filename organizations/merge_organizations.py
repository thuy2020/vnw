from django.core.management.base import BaseCommand, CommandError
from organizations.models import Organization, PersonPosition
from organizations.utils import merge_organizations
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Merge two organizations: keeps the first one, merges the second into it."

    def add_arguments(self, parser):
        parser.add_argument('primary_id', type=int, help='ID of the organization to keep')
        parser.add_argument('duplicate_id', type=int, help='ID of the organization to merge and delete')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be merged without making changes')

    def handle(self, *args, **options):
        primary_id = options['primary_id']
        duplicate_id = options['duplicate_id']
        dry_run = options['dry_run']

        try:
            primary = Organization.objects.get(id=primary_id)
            duplicate = Organization.objects.get(id=duplicate_id)
        except Organization.DoesNotExist:
            raise CommandError("One of the specified organizations does not exist.")

        if primary.id == duplicate.id:
            raise CommandError("Cannot merge the same organization.")

        if dry_run:
            self.stdout.write(self.style.NOTICE("[Dry Run] Preview of what would be merged:"))
            self.stdout.write(f"Primary Org: {primary.name} (ID: {primary.id})")
            self.stdout.write(f"Duplicate Org: {duplicate.name} (ID: {duplicate.id})")

            related_positions = PersonPosition.objects.filter(organization=duplicate)
            self.stdout.write(f"Would reassign {related_positions.count()} PersonPosition(s)")

            if duplicate.description:
                self.stdout.write("Would merge description:")
                self.stdout.write(duplicate.description)

            return

        logger.info(f"Merging Organization #{duplicate_id} ({duplicate.name}) into #{primary_id} ({primary.name})")

        # Merge custom fields
        if not primary.description and duplicate.description:
            primary.description = duplicate.description

        if not primary.function and duplicate.function:
            primary.function = duplicate.function

        primary.save()

        # Update PersonPositions
        PersonPosition.objects.filter(organization=duplicate).update(organization=primary)

        logger.info(f"Reassigned PersonPositions from Org #{duplicate_id} to Org #{primary_id}")

        duplicate.delete()
        logger.info(f"Deleted duplicate organization #{duplicate_id}")

        self.stdout.write(self.style.SUCCESS(f"Successfully merged organization #{duplicate_id} into #{primary_id}"))