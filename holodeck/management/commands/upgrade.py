from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates required database structure and performs pending '\
           'migrations.'

    def handle(self, **options):
        call_command('syncdb', migrate=True)
