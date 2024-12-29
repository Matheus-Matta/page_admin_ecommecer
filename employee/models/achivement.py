from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin


# Modelo conquistas predefinidas
class Achievement(LoggableMixin, models.Model):
    # Conquista pode estar associada a vários funcionários
    employees = models.ManyToManyField(
        "Employee", related_name="achievements", verbose_name=_("Funcionários")
    )
    # Nome da conquista
    name = models.CharField(max_length=255, verbose_name=_("Nome da Conquista"))
    # Imagem associada à conquista
    image = models.ImageField(
        upload_to="employee_achievements/", verbose_name=_("Imagem da Conquista")
    )

    def __str__(self):
        return f"Conquista: {self.name}"
