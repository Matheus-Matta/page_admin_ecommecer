from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import os


class User(AbstractUser):
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


class ActionLog(models.Model):
    # Usuário que realizou a ação
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="action_logs",
        verbose_name=_("User"),
    )
    # Texto descrevendo a ação
    action_text = models.TextField(verbose_name=_("Action Text"))
    # Data e hora da ação
    action_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Action Date"))

    def __str__(self):
        user_info = self.user.username if self.user else "Unknown User"
        if not self.action_text:
            action_text = ""
        else:
            action_text = self.action_text
        return f"Action by {user_info}: {action_text}"
