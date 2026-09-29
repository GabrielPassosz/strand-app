import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
IS_VERCEL = os.getenv("VERCEL") == "1"
if not IS_VERCEL:
    load_dotenv(BASE_DIR / os.getenv("STRAND_ENV_FILE", ".env"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "")
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured(
        "Set a random SECRET_KEY of at least 50 characters. Run python setup_local.py for local setup."
    )
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = [
    s for s in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if s
]
PUBLIC_ORIGIN = os.getenv("PUBLIC_ORIGIN", "http://127.0.0.1:8000").rstrip("/")
if not DEBUG and (
    not PUBLIC_ORIGIN.startswith("https://") or not os.getenv("DATABASE_URL")
):
    raise ImproperlyConfigured(
        "Production requires HTTPS PUBLIC_ORIGIN and DATABASE_URL."
    )
DATA_DIR = Path("/tmp/strand" if IS_VERCEL else os.getenv("DATA_DIR", str(BASE_DIR / "data")))
DATA_DIR.mkdir(parents=True, exist_ok=True)
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.PrivateResponses",
]
ROOT_URLCONF = "strand.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ]
        },
    }
]
WSGI_APPLICATION = "strand.wsgi.application"
DATABASES = {
    "default": dj_database_url.config(
        default=f'sqlite:///{DATA_DIR / "db.sqlite3"}', conn_max_age=0 if IS_VERCEL else 60
    )
}
if DATABASES["default"]["ENGINE"].endswith("sqlite3"):
    DATABASES["default"]["OPTIONS"] = {"timeout": 20}
elif DATABASES["default"]["ENGINE"].endswith("postgresql"):
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True
    DATABASES["default"].setdefault("OPTIONS", {}).update({"prepare_threshold": None, "connect_timeout": 10})
    if os.getenv("DATABASE_SSL_REQUIRED", "True" if IS_VERCEL else "False").lower() == "true":
        DATABASES["default"]["OPTIONS"].setdefault("sslmode", "require")
if IS_VERCEL and (DEBUG or not DATABASES["default"]["ENGINE"].endswith("postgresql")):
    raise ImproperlyConfigured("Vercel requires DEBUG=False and a PostgreSQL DATABASE_URL.")
AUTH_USER_MODEL = "core.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English"), ("pt-br", "Português (Brasil)")]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}
MEDIA_ROOT = DATA_DIR / "private-media"
MEDIA_URL = "/never-public-media/"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 12
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
# Enable only behind a trusted proxy which strips client-provided forwarding headers.
TRUST_PROXY = IS_VERCEL or os.getenv("TRUST_PROXY", "False").lower() == "true"
TRUST_CLIENT_IP_HEADER = os.getenv("TRUST_CLIENT_IP_HEADER", "False").lower() == "true"
if TRUST_PROXY:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
PASSWORD_RESET_TIMEOUT = 3600
MAX_PHOTO_BYTES = 3 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_PHOTO_BYTES
FILE_UPLOAD_PERMISSIONS = 0o600
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o700
DATA_UPLOAD_MAX_NUMBER_FILES = 1
CSRF_FAILURE_VIEW = "core.views.csrf_failure"
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    (
        "django.core.mail.backends.filebased.EmailBackend"
        if DEBUG
        else "django.core.mail.backends.smtp.EmailBackend"
    ),
)
EMAIL_FILE_PATH = DATA_DIR / "emails"
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_TIMEOUT = 15
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Strand <noreply@localhost>")
if not DEBUG and (
    not EMAIL_HOST or not EMAIL_HOST_USER or "@localhost" in DEFAULT_FROM_EMAIL
):
    raise ImproperlyConfigured(
        "Production requires an SMTP service and a verified sender."
    )
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Vercel variables are trusted deployment configuration, never request headers.
from urllib.parse import urlparse
if IS_VERCEL:
    for hostname in [urlparse(PUBLIC_ORIGIN).hostname, os.getenv("VERCEL_URL"), os.getenv("VERCEL_PROJECT_PRODUCTION_URL")]:
        if hostname and hostname not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(hostname)
    CSRF_TRUSTED_ORIGINS = list(set(CSRF_TRUSTED_ORIGINS + [PUBLIC_ORIGIN]))

STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
if STORAGE_BACKEND == "s3":
    required = ["S3_ENDPOINT_URL", "S3_REGION", "S3_ACCESS_KEY_ID", "S3_SECRET_ACCESS_KEY", "S3_BUCKET_NAME"]
    if any(not os.getenv(key) for key in required):
        raise ImproperlyConfigured("Private S3 storage credentials are incomplete.")
    from botocore.config import Config
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "endpoint_url": os.environ["S3_ENDPOINT_URL"],
            "region_name": os.environ["S3_REGION"],
            "access_key": os.environ["S3_ACCESS_KEY_ID"],
            "secret_key": os.environ["S3_SECRET_ACCESS_KEY"],
            "bucket_name": os.environ["S3_BUCKET_NAME"],
            "default_acl": None,
            "file_overwrite": False,
            "querystring_auth": True,
            "querystring_expire": 60,
            "max_memory_size": MAX_PHOTO_BYTES,
            "client_config": Config(signature_version="s3v4", s3={"addressing_style":"path"}, connect_timeout=5, read_timeout=15, retries={"max_attempts":2}, request_checksum_calculation="when_required", response_checksum_validation="when_required"),
            "object_parameters": {"CacheControl":"private, no-store"},
        }
    }
elif STORAGE_BACKEND != "local":
    raise ImproperlyConfigured("STORAGE_BACKEND must be local or s3.")
if IS_VERCEL and STORAGE_BACKEND != "s3":
    raise ImproperlyConfigured("Vercel requires durable private S3 storage.")

CRON_SECRET = os.getenv("CRON_SECRET", "")
