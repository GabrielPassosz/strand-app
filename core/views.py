import json, uuid, io, warnings, logging
from datetime import timedelta
from functools import wraps
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from PIL import Image, ImageOps, UnidentifiedImageError
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone, translation
from django.utils.crypto import salted_hmac
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from .models import User, Client, Visit, Photo, AuditEvent, RateBucket
from .forms import ClientForm, VisitForm, CURRENCIES, DETAILS

logger = logging.getLogger(__name__)
Image.MAX_IMAGE_PIXELS = 20_000_000


def error(code, status=400, **extra):
    return JsonResponse({"error": code, **extra}, status=status)


def csrf_failure(request, reason=""):
    return error("csrf", 403)


def body(request):
    if request.content_type != "application/json":
        raise ValueError("JSON required")
    if len(request.body) > 100_000:
        raise ValueError("Too large")
    data = json.loads(request.body)
    if not isinstance(data, dict):
        raise ValueError("Object required")
    return data


def api(methods, authenticated=True):
    def decorator(func):
        @wraps(func)
        @require_http_methods(methods)
        def wrapped(request, *args, **kwargs):
            if authenticated and (
                not request.user.is_authenticated or not request.user.email_verified
            ):
                return error("unauthorized", 401)
            language = (
                request.user.language
                if request.user.is_authenticated
                else ("pt" if request.headers.get("X-Language") == "pt" else "en")
            )
            with translation.override("pt-br" if language == "pt" else "en"):
                try:
                    return func(request, *args, **kwargs)
                except (ValueError, TypeError, UnicodeError, json.JSONDecodeError):
                    return error("invalid")
                except ValidationError as exc:
                    return error("validation", details=exc.messages)

        return wrapped

    return decorator


def limited(request, scope, identity="", limit=10, seconds=900):
    # Trust X-Real-IP only when deployment explicitly enables the private, controlled proxy.
    source_ip = (request.META.get("HTTP_X_VERCEL_FORWARDED_FOR") or request.META.get("HTTP_X_FORWARDED_FOR")) if settings.IS_VERCEL else (request.META.get("HTTP_X_REAL_IP") if settings.TRUST_CLIENT_IP_HEADER else None)
    who = identity or source_ip or request.META.get("REMOTE_ADDR", "unknown")
    bucket = int(timezone.now().timestamp()) // seconds
    key = salted_hmac("rate", f"{scope}:{who}:{bucket}").hexdigest()
    RateBucket.objects.get_or_create(
        key=key,
        defaults={"expires_at": timezone.now() + timedelta(seconds=seconds * 2)},
    )
    return not RateBucket.objects.filter(key=key, count__lt=limit).update(
        count=F("count") + 1
    )


def audit(user, action, obj=""):
    AuditEvent.objects.create(owner=user, action=action, object_id=str(obj))


def user_data(user):
    return {
        "name": user.first_name,
        "email": user.email,
        "language": user.language,
        "currency": user.currency,
        "timezone": user.timezone,
    }


def client_data(c):
    result = {k: getattr(c, k) for k in ClientForm._meta.fields}
    result.update(
        id=str(c.id),
        version=c.version,
        archived=c.archived,
        birthday=c.birthday.isoformat() if c.birthday else "",
        color="#e5ece3",
    )
    result["visits"] = [
        {
            "id": str(v.id),
            "date": v.date.isoformat(),
            "service": v.service,
            "price": str(v.price),
            "currency": v.currency,
            **v.details,
        }
        for v in c.visits.all()
    ]
    result["photos"] = [
        {
            "id": str(p.id),
            "url": f"/api/photos/{p.id}/",
            "visit_id": str(p.visit_id) if p.visit_id else None,
        }
        for p in c.photos.all()
    ]
    return result


@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")


@api(["GET"], False)
def session(request):
    return JsonResponse(
        {
            "user": (
                user_data(request.user)
                if request.user.is_authenticated and request.user.email_verified
                else None
            )
        }
    )


def deliver(user, kind, link):
    pt = user.language == "pt"
    if kind == "verify":
        subject = "Confirme seu e-mail — Strand" if pt else "Verify your email — Strand"
        text = (
            "Confirme seu e-mail acessando o link abaixo. Ele expira em 24 horas."
            if pt
            else "Verify your email using the link below. It expires in 24 hours."
        )
    else:
        subject = (
            "Redefina sua senha — Strand" if pt else "Reset your password — Strand"
        )
        text = (
            "Redefina sua senha acessando o link abaixo. Ele expira em 1 hora."
            if pt
            else "Reset your password using the link below. It expires in 1 hour."
        )
    suffix = (
        "Se você não solicitou isso, ignore esta mensagem."
        if pt
        else "If you did not request this, ignore this message."
    )
    send_mail(
        subject,
        f"{text}\n\n{link}\n\n{suffix}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


def send_verification(user):
    token = signing.dumps({"id": user.pk, "email": user.email}, salt="verify-email")
    deliver(user, "verify", f"{settings.PUBLIC_ORIGIN}/?verify={token}")


@api(["POST"], False)
def register(request):
    if limited(request, "register", limit=10, seconds=3600):
        return error("rate_limited", 429)
    data = body(request)
    email = str(data.get("email", "")).strip().lower()
    name = str(data.get("name", "")).strip()
    password = data.get("password", "")
    if (
        not name
        or len(name) > 100
        or len(email) > 254
        or not isinstance(password, str)
        or len(password) > 256
    ):
        return error("invalid")
    validate_email(email)
    user = User(
        username=uuid.uuid4().hex,
        email=email,
        first_name=name,
        language="pt" if data.get("language") == "pt" else "en",
        is_active=False,
    )
    validate_password(password, user)
    user.set_password(password)
    if not User.objects.filter(email=email).exists():
        try:
            with transaction.atomic():
                user.save()
        except IntegrityError:
            pass
        else:
            try:
                send_verification(user)
            except Exception:
                logger.warning(
                    "Verification delivery failed; provider configuration must be checked."
                )
                return error("email_unavailable", 503)
    return JsonResponse({"ok": True, "message": "check_email"}, status=202)


@api(["POST"], False)
def resend_verification(request):
    data = body(request)
    email = str(data.get("email", "")).strip().lower()
    if limited(request, "resend-ip", limit=10, seconds=3600) or limited(
        request, "resend-email", email, 3, 3600
    ):
        return error("rate_limited", 429)
    user = User.objects.filter(email=email, email_verified=False).first()
    if user:
        try:
            send_verification(user)
        except Exception:
            return error("email_unavailable", 503)
    return JsonResponse({"ok": True, "message": "check_email"}, status=202)


@api(["POST"], False)
def verify_email(request):
    if limited(request, "verify", limit=30):
        return error("rate_limited", 429)
    data = body(request)
    try:
        payload = signing.loads(
            data.get("token", ""), salt="verify-email", max_age=86400
        )
    except signing.BadSignature:
        return error("invalid_link")
    with transaction.atomic():
        user = (
            User.objects.select_for_update()
            .filter(
                pk=payload.get("id"), email=payload.get("email"), email_verified=False
            )
            .first()
        )
        if not user:
            return error("invalid_link")
        user.email_verified = True
        user.is_active = True
        user.save(update_fields=["email_verified", "is_active"])
        audit(user, "email_verified")
    return JsonResponse({"ok": True})


@api(["POST"], False)
def sign_in(request):
    data = body(request)
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    if limited(request, "login-ip", limit=100) or limited(
        request, "login-email", email, 10
    ):
        return error("rate_limited", 429)
    if not isinstance(password, str) or len(password) > 256:
        return error("invalid_credentials", 401)
    found = User.objects.filter(email=email).first()
    user = authenticate(
        request, username=found.username if found else "__missing__", password=password
    )
    if not user or not user.email_verified:
        return error("invalid_credentials", 401)
    login(request, user)
    audit(user, "login")
    return JsonResponse({"user": user_data(user)})


@api(["POST"])
def sign_out(request):
    audit(request.user, "logout")
    logout(request)
    return JsonResponse({"ok": True})


@api(["POST"], False)
def reset_request(request):
    data = body(request)
    email = str(data.get("email", "")).strip().lower()
    if limited(request, "reset-ip", limit=10, seconds=3600) or limited(
        request, "reset-email", email, 3, 3600
    ):
        return error("rate_limited", 429)
    user = User.objects.filter(email=email, is_active=True, email_verified=True).first()
    if user:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        try:
            deliver(user, "reset", f"{settings.PUBLIC_ORIGIN}/?uid={uid}&reset={token}")
        except Exception:
            return error("email_unavailable", 503)
    return JsonResponse({"ok": True, "message": "check_email"}, status=202)


@api(["POST"], False)
def reset_confirm(request):
    if limited(request, "reset-confirm", limit=30):
        return error("rate_limited", 429)
    data = body(request)
    try:
        uid = urlsafe_base64_decode(data.get("uid", "")).decode()
    except (ValueError, TypeError, OverflowError, UnicodeError):
        return error("invalid_link")
    with transaction.atomic():
        try:
            user = User.objects.select_for_update().get(
                pk=uid, is_active=True, email_verified=True
            )
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return error("invalid_link")
        if not default_token_generator.check_token(user, data.get("token", "")):
            return error("invalid_link")
        password = data.get("password", "")
        if not isinstance(password, str) or len(password) > 256:
            return error("invalid")
        validate_password(password, user)
        user.set_password(password)
        user.save(update_fields=["password"])
        audit(user, "password_reset")
    return JsonResponse({"ok": True})


@api(["POST"])
def password_change(request):
    data = body(request)
    if limited(request, "password-change", str(request.user.pk), 5):
        return error("rate_limited", 429)
    if not request.user.check_password(data.get("current_password", "")):
        return error("invalid_credentials", 400)
    password = data.get("password", "")
    if not isinstance(password, str) or len(password) > 256:
        return error("invalid")
    validate_password(password, request.user)
    request.user.set_password(password)
    request.user.save(update_fields=["password"])
    update_session_auth_hash(request, request.user)
    audit(request.user, "password_changed")
    return JsonResponse({"ok": True})


@api(["PATCH"])
def preferences(request):
    data = body(request)
    if (
        data.get("language") not in ["en", "pt"]
        or data.get("currency") not in CURRENCIES
    ):
        return error("invalid")
    try:
        ZoneInfo(data.get("timezone", ""))
    except (ZoneInfoNotFoundError, ValueError):
        return error("invalid")
    for key in ["language", "currency", "timezone"]:
        setattr(request.user, key, data[key])
    request.user.save(update_fields=["language", "currency", "timezone"])
    return JsonResponse({"user": user_data(request.user)})


@api(["GET", "POST"])
def client_list(request):
    if request.method == "GET":
        qs = Client.objects.filter(owner=request.user).prefetch_related(
            "visits", "photos"
        )
        return JsonResponse({"clients": [client_data(c) for c in qs]})
    data = body(request)
    form = ClientForm(data)
    if not form.is_valid():
        return error("validation", fields=form.errors.get_json_data())
    with transaction.atomic():
        c = form.save(commit=False)
        c.owner = request.user
        c.save()
        audit(request.user, "client_created", c.pk)
    return JsonResponse({"client": client_data(c)}, status=201)


@api(["PATCH"])
def client_detail(request, pk):
    data = body(request)
    with transaction.atomic():
        c = get_object_or_404(
            Client.objects.select_for_update(), id=pk, owner=request.user
        )
        if data.get("version") != c.version:
            return error("conflict", 409)
        if "archived" in data:
            if not isinstance(data["archived"], bool):
                return error("invalid")
            c.archived = data["archived"]
        else:
            form = ClientForm(data, instance=c)
            if not form.is_valid():
                return error("validation", fields=form.errors.get_json_data())
            c = form.save(commit=False)
        c.version += 1
        c.save()
        audit(request.user, "client_updated", c.pk)
    return JsonResponse({"client": client_data(c)})


@api(["POST"])
def visit_create(request, pk):
    c = get_object_or_404(Client, id=pk, owner=request.user, archived=False)
    form = VisitForm(body(request))
    if not form.is_valid():
        return error("validation", fields=form.errors.get_json_data())
    d = form.cleaned_data
    details = {k: str(d[k]) for k in DETAILS if d.get(k) is not None and d[k] != ""}
    with transaction.atomic():
        visit, created = Visit.objects.get_or_create(
            client=c,
            request_id=d["request_id"],
            defaults={
                **{k: d[k] for k in ["date", "service", "price", "currency"]},
                "details": details,
            },
        )
        if created:
            audit(request.user, "visit_created", visit.pk)
    return JsonResponse({"client": client_data(c)}, status=201 if created else 200)


@api(["POST"])
def photo_create(request, pk):
    c = get_object_or_404(Client, id=pk, owner=request.user, archived=False)
    if limited(request, "upload", str(request.user.pk), 60, 3600):
        return error("rate_limited", 429)
    upload = request.FILES.get("photo")
    if not upload or upload.size > settings.MAX_PHOTO_BYTES:
        return error("invalid_photo")
    visit = None
    if request.POST.get("visit_id"):
        visit = get_object_or_404(Visit, id=request.POST["visit_id"], client=c)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(upload) as im:
                if im.format not in ["JPEG", "PNG", "WEBP"]:
                    return error("invalid_photo")
                im.load()
                im = ImageOps.exif_transpose(im).convert("RGB")
                im.thumbnail((2400, 2400))
                output = io.BytesIO()
                im.save(output, "JPEG", quality=88)
                if output.tell() > settings.MAX_PHOTO_BYTES:
                    return error("invalid_photo")
    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombWarning,
        Image.DecompressionBombError,
    ):
        return error("invalid_photo")
    photo = Photo(client=c, visit=visit)
    photo.image.save(
        f"{uuid.uuid4().hex}.jpg", ContentFile(output.getvalue()), save=False
    )
    try:
        with transaction.atomic():
            photo.save()
            audit(request.user, "photo_created", photo.pk)
    except Exception:
        photo.image.delete(save=False)
        raise
    return JsonResponse({"client": client_data(c)}, status=201)


@api(["GET", "DELETE"])
def photo_detail(request, pk):
    p = get_object_or_404(
        Photo.objects.select_related("client"), id=pk, client__owner=request.user
    )
    if request.method == "DELETE":
        storage = p.image.storage
        name = p.image.name
        with transaction.atomic():
            audit(request.user, "photo_deleted", p.pk)
            p.delete()
            transaction.on_commit(lambda: storage.delete(name))
        return JsonResponse({"ok": True})
    try:
        response = FileResponse(p.image.open("rb"), content_type="image/jpeg")
    except FileNotFoundError:
        return error("not_found", 404)
    response["Content-Disposition"] = 'inline; filename="photo.jpg"'
    return response


@api(["GET"])
def export_data(request):
    qs = Client.objects.filter(owner=request.user).prefetch_related("visits", "photos")
    response = JsonResponse(
        {"profile": user_data(request.user), "clients": [client_data(c) for c in qs]}
    )
    response["Content-Disposition"] = 'attachment; filename="strand-records.json"'
    return response


@require_http_methods(["GET"])
def maintenance(request):
    from django.utils.crypto import constant_time_compare
    from django.contrib.sessions.models import Session
    expected = settings.CRON_SECRET
    if not expected or not constant_time_compare(request.headers.get("Authorization", ""), "Bearer " + expected):
        return error("unauthorized", 401)
    RateBucket.objects.filter(expires_at__lt=timezone.now()).delete()
    Session.objects.filter(expire_date__lt=timezone.now()).delete()
    return JsonResponse({"ok": True})
