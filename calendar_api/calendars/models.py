import uuid
from django.db import models
from django.utils import timezone
from calendar_api.config.common import Common


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Calendar(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Common.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    timezone = models.CharField(default="UTC", max_length=100)


class Event(TimeStampMixin):
    CONFIRMED = 'confirmed'
    TENTATIVE = 'tentative'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = (
        (CONFIRMED, 'Confirmed'),
        (TENTATIVE, 'Tentative'),
        (CANCELLED, 'Cancelled')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=TENTATIVE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
