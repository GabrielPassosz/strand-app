import uuid
from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    language = models.CharField(max_length=2, default="en")
    currency = models.CharField(max_length=3, default="USD")
    timezone = models.CharField(max_length=80, default="America/New_York")
    email_verified = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("email"), name="user_email_lower_unique")
        ]


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients")
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    birthday = models.DateField(null=True, blank=True)
    texture = models.CharField(max_length=20, blank=True)
    pattern = models.CharField(max_length=20, blank=True)
    length = models.CharField(max_length=20, blank=True)
    porosity = models.CharField(max_length=20, blank=True)
    elasticity = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True, max_length=4000)
    archived = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["owner", "archived", "name"])]
        ordering = ["name"]


class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="visits")
    date = models.DateField()
    service = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    details = models.JSONField(default=dict)
    request_id = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["client", "request_id"], name="visit_idempotency"
            )
        ]


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="photos")
    visit = models.ForeignKey(
        Visit, null=True, blank=True, on_delete=models.SET_NULL, related_name="photos"
    )
    image = models.FileField(upload_to="photos/%Y/%m/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class AuditEvent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=40)
    object_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RateBucket(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(db_index=True)
