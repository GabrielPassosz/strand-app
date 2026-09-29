from importlib import import_module
from django.apps import apps
from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Enable RLS and remove anonymous API grants from all Django application tables.'
    def handle(self, *args, **options):
        if connection.vendor != 'postgresql':
            self.stdout.write('SQLite local: no external Data API grants to revoke.')
            return
        with connection.schema_editor() as editor:
            import_module('core.migrations.0002_protect_postgres').protect(apps, editor)
        self.stdout.write('Django tables protected. Backend must connect as their owning database role.')
