from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the database tables for holodeck.models.Sample in shards whose tables haven't already been created."

    def handle(self, *args, **options):
        for database_name, database_settings in settings.DATABASES.items():
            if database_name.startswith('shard_'):
                print 'Syncing %s...' % database_name
                management.call_command('syncdb', database=database_name)
