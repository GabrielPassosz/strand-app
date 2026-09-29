from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from core.models import RateBucket


class Command(BaseCommand):
    help = "Delete expired sessions and rate-limit buckets. Run daily."

    def handle(self, *args, **options):
        call_command("clearsessions")
        count, _ = RateBucket.objects.filter(expires_at__lt=timezone.now()).delete()
        self.stdout.write(f"Removed {count} expired rate-limit buckets.")
