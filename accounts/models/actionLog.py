from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User


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
    # Status HTTP da ação
    status_code = models.IntegerField(
        null=True, blank=True, verbose_name=_("HTTP Status Code")
    )

    def __str__(self):
        user_info = self.user.username if self.user else "Unknown User"
        if not self.action_text:
            action_text = ""
        else:
            action_text = self.action_text
        return f"Action by {user_info}: {action_text}"
