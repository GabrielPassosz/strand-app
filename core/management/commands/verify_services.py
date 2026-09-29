import uuid
from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import connection
from django.core.mail import send_mail
from django.conf import settings
from core.models import Client

class Command(BaseCommand):
    help = 'Verify the real configured database and private storage. Optionally send a test email.'
    def add_arguments(self, parser):
        parser.add_argument('--storage', action='store_true')
        parser.add_argument('--email', default='')
    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                if cursor.fetchone()[0] != 1:
                    raise CommandError('Database check failed.')
            Client.objects.exists()
            self.stdout.write('Database connection and client table: OK')
            if options['storage']:
                key = None
                marker = b'Strand deployment connectivity check'
                try:
                    key = default_storage.save('checks/' + uuid.uuid4().hex + '.txt', ContentFile(marker))
                    with default_storage.open(key, 'rb') as stream:
                        if stream.read() != marker:
                            raise CommandError('Storage content mismatch.')
                    self.stdout.write('Storage upload and read: OK')
                finally:
                    if key:
                        default_storage.delete(key)
                self.stdout.write('Storage delete: OK. Verify the bucket is PRIVATE in Supabase.')
            if options['email']:
                send_mail('Strand: teste de configuração / configuration test', 'A configuração de envio do Strand foi testada. / Strand email configuration was tested.', settings.DEFAULT_FROM_EMAIL, [options['email']])
                self.stdout.write('Email accepted by the configured backend. Confirm receipt in your inbox.')
        except CommandError:
            raise
        except Exception as exc:
            # Provider exceptions may contain sensitive connection parameters; do not echo them.
            raise CommandError('Service check failed (' + type(exc).__name__ + '). Check private provider configuration.') from None
