import json, sqlite3, tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = "Back up the local SQLite database and private photos. Stop application writes first."

    def add_arguments(self, parser):
        parser.add_argument("--output", required=True)

    def handle(self, *args, **options):
        db = settings.DATABASES["default"]
        if not db["ENGINE"].endswith("sqlite3"):
            raise CommandError(
                "Use pg_dump for PostgreSQL and back up private-media separately."
            )
        output = Path(options["output"]).resolve()
        media = Path(settings.MEDIA_ROOT).resolve()
        if output.is_relative_to(media):
            raise CommandError("Backup cannot be stored inside private-media.")
        if output.exists():
            raise CommandError("Output already exists. Choose a new backup filename.")
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp) / "db.sqlite3"
            source = sqlite3.connect(str(db["NAME"]))
            target = sqlite3.connect(str(snapshot))
            try:
                source.backup(target)
            finally:
                source.close()
                target.close()
            with ZipFile(output, "x", ZIP_DEFLATED) as archive:
                archive.write(snapshot, "db.sqlite3")
                if media.exists():
                    for path in media.rglob("*"):
                        if path.is_file():
                            archive.write(
                                path,
                                "private-media/" + path.relative_to(media).as_posix(),
                            )
                archive.writestr(
                    "backup.json",
                    json.dumps(
                        {
                            "created_at": timezone.now().isoformat(),
                            "application": "Strand",
                            "schema": "Django migrations included in source package",
                        }
                    ),
                )
        self.stdout.write(str(output))
