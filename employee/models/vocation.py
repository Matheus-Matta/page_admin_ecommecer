from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin
from .employee import Employee
from datetime import timedelta


# Modelo para registrar informações de férias
class Vacation(LoggableMixin, models.Model):

    # Relaciona as férias ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="vacations"
    )

    # Data de início das férias
    start_date = models.DateField(verbose_name=_("Data de Início"))

    # Data de término das férias
    end_date = models.DateField(verbose_name=_("Data de Fim"))

    # Número total de dias disponíveis para férias (por período aquisitivo)
    total_days_available = models.PositiveIntegerField(
        verbose_name=_("Dias Disponíveis"), default=30
    )

    # Número de dias de férias utilizados
    days_taken = models.PositiveIntegerField(verbose_name=_("Dias Usados"), default=0)

    # Observações adicionais
    observation = models.TextField(blank=True, null=True, verbose_name=_("Observação"))

    # Status das férias
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pendente"),
            ("approved", "Aprovado"),
            ("rejected", "Rejeitado"),
            ("completed", "Concluído"),
        ],
        default="pending",
        verbose_name=_("Status"),
    )

    class Meta:
        verbose_name = _("Férias")
        verbose_name_plural = _("Férias")
        ordering = ["-start_date"]

    def __str__(self):
        return f"Férias de {self.employee.user.full_name} ({self.start_date} a {self.end_date})"

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para calcular automaticamente os dias usados
        com base nas datas de início e término, se não fornecidos.
        """
        if self.start_date and self.end_date:
            calculated_days = (self.end_date - self.start_date).days + 1
            if self.days_taken == 0:  # Se não especificado, calcula automaticamente
                self.days_taken = calculated_days

            # Valida se os dias utilizados excedem os disponíveis
            if self.days_taken > self.total_days_available:
                raise ValueError(
                    _("Os dias utilizados não podem exceder os dias disponíveis.")
                )

        super().save(*args, **kwargs)

    def remaining_days(self):
        """
        Retorna o número de dias restantes para férias no período atual.
        """
        return self.total_days_available - self.days_taken

    def is_within_period(self, date):
        """
        Verifica se uma data está dentro do período de férias.
        """
        return self.start_date <= date <= self.end_date
