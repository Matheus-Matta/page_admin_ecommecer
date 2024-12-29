from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin
from .employee import Employee


# Modelo para registrar adiantamentos feitos ao funcionário
class Advance(LoggableMixin, models.Model):
    # Relaciona o adiantamento ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="advances"
    )
    # Valor do adiantamento
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Valor")
    )
    # Data em que o adiantamento foi realizado
    date = models.DateField(verbose_name=_("Data"))
    # Descrição opcional do adiantamento
    description = models.CharField(
        max_length=255, verbose_name=_("Descrição"), blank=True, null=True
    )

    def __str__(self):
        return f"Adiantamento para {self.employee.user.full_name} - {self.amount}"
