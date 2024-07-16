from django.db import models
from django.utils import timezone
from datetime import timedelta

import uuid


# Create your models here.
class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    expiration_date = models.DateTimeField(
        "expiration_date", default=timezone.now() + timedelta(days=30)
    )
    current_views = models.IntegerField(default=0)
    max_views = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def is_expired(self):
        if self.expiration_date and self.expiration_date < timezone.now():
            return True
        if self.current_views >= self.max_views:
            return True
        return False
