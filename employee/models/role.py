from django.db import models
from accounts.mixin import LoggableMixin
from .permission import Permission
from django.utils.translation import gettext_lazy as _


# Modelo de Cargo
class Role(LoggableMixin, models.Model):
    # Nome do cargo
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    # Abreviação do cargo
    code = models.CharField(max_length=2, verbose_name=_("Codigo"))
    # Permissões associadas ao cargo
    permissions = models.ManyToManyField(
        Permission,
        related_name="roles_permissions",
        verbose_name=_("cargo_permissions"),
    )

    def __str__(self):
        return self.name
