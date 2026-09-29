> Vercel / Supabase / Netlify: consulte `GUIA_PUBLICACAO.md` para a configuração cloud desta versão. Cobrança automática continua pendente.

# Strand — functional application, v0.2.0

A client-folio application for independent hairstylists. English is the default interface language; Brazilian Portuguese is fully available. This release has a real Django backend and durable data, unlike the earlier frontend prototype.

## Run locally

Use Python 3.12 or 3.13. On Windows, extract the full archive and run `start_windows.bat`. Open http://127.0.0.1:8000 and create an account.

Local development writes verification and recovery emails to `data/emails/`; it does not send them to an inbox. Open the latest email file, follow its verification link, and sign in. No preconfigured user or demo password is provided.

Manual setup:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python setup_local.py
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

On Windows use `.venv\Scripts\python.exe`. Keep the server running while using the application. Data persists after closing it. Do not open the template as a standalone HTML file.

## Included

Verified-email signup, sign-in/out, password recovery/change, owner-scoped client records, hair profiles, permanent visit history, formulas, service amounts, private image uploads, visit-linked photos, client archiving/restoration, JSON data export, language/currency/time-zone preferences, audit records, CSRF protection, input validation, login rate limits, edit-conflict detection and idempotent visit submission.

Uploaded photos are re-encoded to JPEG with metadata removed and a maximum dimension of 2400 pixels. Original image files are not retained. Free-text notes are not automatically translated; changing currency does not convert old records.

## Online deployment and remaining work

The functional application has not been published to the earlier prototype URL. A Linux/Docker deployment configuration with PostgreSQL, private file storage and an HTTPS proxy is included. You must provide your own server, domain and SMTP service and validate them after deployment. See `DEPLOYMENT.md` for commands and operations guidance.

Automated subscription billing is not implemented. The application explicitly shows early access with no automatic charges. Checkout, payment-provider integration, signed webhooks and subscription access rules require a commercial account and plan decisions.

There is no scheduling calendar, salon/team management, MFA, full account/client erasure flow, automatic backup scheduler or high-availability deployment. Archiving keeps data. Review these limits before commercial release.

## Data and maintenance

Local data is stored in `data/db.sqlite3` and `data/private-media/`. `.env` contains your secret key and must remain private. Production uses persistent PostgreSQL and media volumes. Never expose media directories directly.

Run tests with `python manage.py test core`. Run `python manage.py maintenance` daily in production. Stop application writes before running `python manage.py backup_local --output backups/strand-backup.zip` for SQLite. For PostgreSQL use `pg_dump` and a matching copy of private media. Backups must be protected and restore-tested; the included tool does not encrypt them.

See `VALIDATION.md` for the verification scope. This is a tested first functional release, not a claim of an independent security audit or a completed public commercial launch.
