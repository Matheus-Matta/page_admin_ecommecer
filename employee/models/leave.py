from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin
from .employee import Employee
from datetime import timedelta, date


class Leave(LoggableMixin, models.Model):
    # Relaciona a licença ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="leaves"
    )

    # Tipo de licença (ex.: médica ou pessoal)
    leave_type = models.CharField(
        max_length=50,
        choices=[
            ("sick", "Licença Médica"),
            ("personal", "Licença Pessoal"),
            ("maternity", "Licença Maternidade"),
            ("paternity", "Licença Paternidade"),
        ],
        verbose_name=_("Tipo de Licença"),
    )

    # Data de início da licença
    start_date = models.DateField(verbose_name=_("Data de Início"))

    # Data de término da licença
    end_date = models.DateField(verbose_name=_("Data de Fim"))

    # Status da licença (aprovada ou pendente)
    status = models.CharField(
        max_length=10,
        choices=[
            ("approved", "Aprovado"),
            ("pending", "Pendente"),
            ("rejected", "Rejeitado"),
        ],
        default="pending",
        verbose_name=_("Status"),
    )

    # Observações ou detalhes adicionais sobre a licença
    observation = models.TextField(blank=True, null=True, verbose_name=_("Observação"))

    class Meta:
        verbose_name = _("Licença")
        verbose_name_plural = _("Licenças")
        ordering = ["-start_date"]

    def __str__(self):
        return f"Licença de {self.employee.user.full_name} ({self.start_date} a {self.end_date})"

    def total_days(self):
        """
        Calcula o número total de dias de licença.
        """
        return (self.end_date - self.start_date).days + 1

    def is_active(self):
        """
        Verifica se a licença está ativa no dia atual.
        """
        today = date.today()
        return self.start_date <= today <= self.end_date
