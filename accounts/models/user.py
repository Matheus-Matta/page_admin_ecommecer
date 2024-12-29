from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from accounts.mixin import LoggableMixin
import os


class User(LoggableMixin, AbstractUser):
    # Adicionando um campo personalizado
    full_name = models.CharField(
        max_length=255, verbose_name=_("Full Name"), blank=True, null=True
    )
    profile = models.ImageField(upload_to="profile/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.profile:
            filename, file_extension = os.path.splitext(self.profile.name)
            timestamp = int(timezone.now().timestamp())
            self.profile.name = f"profile_{timestamp}{file_extension}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.username
