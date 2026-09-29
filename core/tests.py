import io, json, re, tempfile, uuid
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from PIL import Image
from django.test import TestCase, Client as Browser, override_settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import User, Client, Visit, Photo

PASSWORD = "Strand!Testing92-green"


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    SECURE_SSL_REDIRECT=False,
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    },
)
class AppTests(TestCase):
    def setUp(self):
        self.media = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.addCleanup(self.media.cleanup)
        self.a = User.objects.create_user(
            username="a",
            email="a@example.com",
            password=PASSWORD,
            email_verified=True,
            first_name="A",
        )
        self.b = User.objects.create_user(
            username="b",
            email="b@example.com",
            password=PASSWORD,
            email_verified=True,
            first_name="B",
        )
        self.browser = Browser()
        self.browser.force_login(self.a)
        self.record = Client.objects.create(
            owner=self.a, name="Only A", notes="Private note"
        )

    def send(self, path, data, browser=None, method="post"):
        return getattr(browser or self.browser, method)(
            path, json.dumps(data), content_type="application/json"
        )

    def image(self):
        out = io.BytesIO()
        Image.new("RGB", (20, 20), "red").save(out, "PNG")
        return SimpleUploadedFile("photo.png", out.getvalue(), content_type="image/png")

    def test_registration_verification_login(self):
        browser = Browser()
        payload = {
            "name": "Maria",
            "email": "MARIA@example.com",
            "password": PASSWORD,
            "language": "pt",
        }
        response = self.send("/api/auth/register/", payload, browser)
        self.assertEqual(response.status_code, 202)
        u = User.objects.get(email="maria@example.com")
        self.assertFalse(u.is_active)
        self.assertFalse(u.is_staff)
        self.assertNotEqual(u.password, PASSWORD)
        self.assertEqual(
            self.send("/api/auth/login/", payload, browser).status_code, 401
        )
        self.assertIn("Confirme", mail.outbox[0].subject)
        link = re.search(r"https?://\S+", mail.outbox[0].body).group()
        token = parse_qs(urlparse(link).query)["verify"][0]
        self.assertEqual(
            self.send("/api/auth/verify/", {"token": token}, browser).status_code, 200
        )
        self.assertEqual(
            self.send("/api/auth/verify/", {"token": token}, browser).status_code, 400
        )
        self.assertEqual(
            self.send("/api/auth/login/", payload, browser).status_code, 200
        )

    def test_duplicate_registration_and_weak_password(self):
        browser = Browser()
        self.assertEqual(
            self.send(
                "/api/auth/register/",
                {"name": "New", "email": "A@example.com", "password": PASSWORD},
                browser,
            ).status_code,
            202,
        )
        self.assertEqual(User.objects.filter(email__iexact="a@example.com").count(), 1)
        self.assertEqual(
            self.send(
                "/api/auth/register/",
                {"name": "New", "email": "new@example.com", "password": "123"},
                browser,
            ).status_code,
            400,
        )

    def test_anonymous_cannot_read_or_write(self):
        b = Browser()
        self.assertEqual(b.get("/api/clients/").status_code, 401)
        self.assertEqual(self.send("/api/clients/", {"name": "No"}, b).status_code, 401)
        self.assertEqual(b.get("/api/export/").status_code, 401)

    def test_csrf_required_on_login_and_mutations(self):
        b = Browser(enforce_csrf_checks=True)
        self.assertEqual(
            self.send(
                "/api/auth/login/", {"email": self.a.email, "password": PASSWORD}, b
            ).status_code,
            403,
        )
        b.force_login(self.a)
        self.assertEqual(self.send("/api/clients/", {"name": "No"}, b).status_code, 403)

    def test_csrf_valid_request(self):
        b = Browser(enforce_csrf_checks=True)
        b.force_login(self.a)
        b.get("/")
        response = b.post(
            "/api/clients/",
            json.dumps({"name": "Yes"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=b.cookies["csrftoken"].value,
        )
        self.assertEqual(response.status_code, 201)

    def test_owner_cannot_be_forged(self):
        r = self.send(
            "/api/clients/", {"name": "New", "owner": self.b.pk, "is_staff": True}
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(
            Client.objects.get(pk=r.json()["client"]["id"]).owner_id, self.a.pk
        )

    def test_isolation_listing_edit_visit_export(self):
        self.browser.force_login(self.b)
        self.assertEqual(self.browser.get("/api/clients/").json()["clients"], [])
        self.assertEqual(
            self.send(
                f"/api/clients/{self.record.pk}/",
                {"name": "Stolen", "version": 1},
                method="patch",
            ).status_code,
            404,
        )
        self.assertEqual(
            self.send(f"/api/clients/{self.record.pk}/visits/", {}).status_code, 404
        )
        self.assertEqual(self.browser.get("/api/export/").json()["clients"], [])
        self.record.refresh_from_db()
        self.assertEqual(self.record.name, "Only A")

    def test_persistence_edit_conflict_and_archive_restore(self):
        url = f"/api/clients/{self.record.pk}/"
        self.assertEqual(
            self.send(
                url, {"name": "Changed", "version": 1}, method="patch"
            ).status_code,
            200,
        )
        self.assertEqual(
            self.send(url, {"name": "Stale", "version": 1}, method="patch").status_code,
            409,
        )
        self.assertEqual(
            self.send(
                url, {"archived": True, "version": 2}, method="patch"
            ).status_code,
            200,
        )
        self.assertEqual(self.send(f"{url}visits/", {}).status_code, 404)
        self.assertEqual(
            self.send(
                url, {"archived": False, "version": 3}, method="patch"
            ).status_code,
            200,
        )
        b = Browser()
        b.force_login(self.a)
        self.assertEqual(b.get("/api/clients/").json()["clients"][0]["name"], "Changed")

    def test_visit_idempotency_money_and_data(self):
        data = {
            "service": "colorService",
            "date": "2026-09-26",
            "price": "125.50",
            "currency": "BRL",
            "formula": "6N + 10 vol",
            "request_id": str(uuid.uuid4()),
        }
        url = f"/api/clients/{self.record.pk}/visits/"
        self.assertEqual(self.send(url, data).status_code, 201)
        self.assertEqual(self.send(url, data).status_code, 200)
        self.assertEqual(Visit.objects.count(), 1)
        v = Visit.objects.get()
        self.assertEqual(str(v.price), "125.50")
        self.assertEqual(v.details["formula"], data["formula"])
        data["request_id"] = str(uuid.uuid4())
        data["price"] = "-1"
        self.assertEqual(self.send(url, data).status_code, 400)
        data["price"] = "20"
        data["date"] = "not-a-date"
        self.assertEqual(self.send(url, data).status_code, 400)

    def test_photo_private_cross_account_and_delete(self):
        r = self.browser.post(
            f"/api/clients/{self.record.pk}/photos/", {"photo": self.image()}
        )
        self.assertEqual(r.status_code, 201)
        p = Photo.objects.get()
        url = f"/api/photos/{p.pk}/"
        path = Path(p.image.path)
        response = self.browser.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/jpeg")
        self.assertIn("no-store", response["Cache-Control"])
        response.close()
        self.assertEqual(Browser().get(url).status_code, 401)
        self.browser.force_login(self.b)
        self.assertEqual(self.browser.get(url).status_code, 404)
        self.assertEqual(self.browser.delete(url).status_code, 404)
        self.browser.force_login(self.a)
        with self.captureOnCommitCallbacks(execute=True):
            self.assertEqual(self.browser.delete(url).status_code, 200)
        self.assertFalse(path.exists())

    def test_photo_rejects_script_and_wrong_visit(self):
        url = f"/api/clients/{self.record.pk}/photos/"
        fake = SimpleUploadedFile(
            "attack.jpg", b"<script>alert(1)</script>", content_type="image/jpeg"
        )
        self.assertEqual(self.browser.post(url, {"photo": fake}).status_code, 400)
        other = Client.objects.create(owner=self.b, name="B")
        visit = Visit.objects.create(
            client=other,
            date="2026-09-26",
            price=10,
            currency="USD",
            service="cutService",
        )
        self.assertEqual(
            self.browser.post(
                url, {"photo": self.image(), "visit_id": str(visit.pk)}
            ).status_code,
            404,
        )
        self.assertEqual(Photo.objects.count(), 0)

    def test_password_reset_one_time_and_sessions_invalidated(self):
        old = Browser()
        old.force_login(self.a)
        anon = Browser()
        self.assertEqual(
            self.send("/api/auth/reset/", {"email": self.a.email}, anon).status_code,
            202,
        )
        link = re.search(r"https?://\S+", mail.outbox[-1].body).group()
        qs = parse_qs(urlparse(link).query)
        data = {
            "uid": qs["uid"][0],
            "token": qs["reset"][0],
            "password": "Replacement!Strong2026",
        }
        self.assertEqual(
            self.send("/api/auth/reset-confirm/", data, anon).status_code, 200
        )
        self.assertEqual(
            self.send("/api/auth/reset-confirm/", data, anon).status_code, 400
        )
        self.assertEqual(old.get("/api/clients/").status_code, 401)

    def test_password_change_preserves_current_session_only(self):
        other = Browser()
        other.force_login(self.a)
        self.assertEqual(
            self.send(
                "/api/auth/password/",
                {"current_password": PASSWORD, "password": "Replacement!Strong2026"},
            ).status_code,
            200,
        )
        self.assertEqual(self.browser.get("/api/clients/").status_code, 200)
        self.assertEqual(other.get("/api/clients/").status_code, 401)

    def test_rate_limit_login(self):
        b = Browser()
        for _ in range(10):
            self.assertEqual(
                self.send(
                    "/api/auth/login/", {"email": self.a.email, "password": "wrong"}, b
                ).status_code,
                401,
            )
        self.assertEqual(
            self.send(
                "/api/auth/login/", {"email": self.a.email, "password": PASSWORD}, b
            ).status_code,
            429,
        )

    def test_preferences_persist_and_reject_invalid(self):
        payload = {"language": "pt", "currency": "BRL", "timezone": "America/Sao_Paulo"}
        self.assertEqual(
            self.send("/api/preferences/", payload, method="patch").status_code, 200
        )
        self.a.refresh_from_db()
        self.assertEqual(self.a.language, "pt")
        payload["timezone"] = "not/real"
        self.assertEqual(
            self.send("/api/preferences/", payload, method="patch").status_code, 400
        )

    def test_logout_and_no_public_media(self):
        self.assertEqual(self.send("/api/auth/logout/", {}).status_code, 200)
        self.assertEqual(self.browser.get("/api/clients/").status_code, 401)
        self.assertEqual(
            self.browser.get("/never-public-media/test.jpg").status_code, 404
        )

    def test_invalid_shapes_and_invalid_photo_uuid(self):
        self.assertEqual(
            self.browser.post(
                "/api/clients/", "[]", content_type="application/json"
            ).status_code,
            400,
        )
        self.assertEqual(
            self.send("/api/clients/", {"name": "A", "email": "invalid"}).status_code,
            400,
        )
        self.assertEqual(
            self.send(
                "/api/clients/", {"name": "A", "texture": "anything"}
            ).status_code,
            400,
        )

    def test_empty_real_account_no_demo_records(self):
        self.browser.force_login(self.b)
        r = self.browser.get("/api/clients/")
        self.assertEqual(r.json()["clients"], [])
        self.assertNotIn("Olivia", r.content.decode())
