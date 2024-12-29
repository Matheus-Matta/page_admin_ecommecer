from django.db import models
from .user import User
from django.utils.translation import gettext_lazy as _


class UserSessionLog(models.Model):
    class ActionChoices(models.TextChoices):
        LOGIN = "login", _("Login")
        LOGOUT = "logout", _("Logout")
        EXPIRED = "expired", _("Sessão Expirada")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="session_logs",
        verbose_name=_("User"),
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP Address"), null=True, blank=True
    )
    location = models.CharField(
        max_length=255, verbose_name=_("Location"), null=True, blank=True
    )
    action = models.CharField(
        max_length=20, choices=ActionChoices.choices, verbose_name=_("Action")
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Timestamp"))

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.timestamp}"
