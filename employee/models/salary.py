from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin


class Salary(LoggableMixin, models.Model):

    # Data de início da vigência do salário
    start_date = models.DateField(verbose_name=_("Data de Início"))

    # Data de término da vigência do salário (opcional)
    end_date = models.DateField(
        blank=True, null=True, verbose_name=_("Data de Término")
    )

    # Valor bruto do salário
    gross_salary = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Salário Bruto")
    )


# Modelo de Aplicação de Descontos
class SalaryAdjustment(LoggableMixin, models.Model):
    """
    Modelo para armazenar ajustes de salário (adições ou subtrações).
    """

    ADJUSTMENT_TYPE_CHOICES = [
        ("add", "Adição"),
        ("subtract", "Subtração"),
    ]

    salary = models.ForeignKey(
        Salary,
        on_delete=models.CASCADE,
        related_name="adjustments",
        verbose_name=_("Salário"),
    )

    # Tipo de ajuste: adição ou subtração
    adjustment_type = models.CharField(
        max_length=10,
        choices=ADJUSTMENT_TYPE_CHOICES,
        verbose_name=_("Tipo de Ajuste"),
    )

    # Valor do ajuste
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Valor do Ajuste"),
    )

    # Descrição do ajuste (ex.: falta, vale, gratificação)
    description = models.CharField(
        max_length=255,
        verbose_name=_("Descrição"),
        help_text=_("Descrição do ajuste, ex.: falta, vale, comissão"),
    )

    # Observação adicional
    observation = models.TextField(blank=True, null=True, verbose_name=_("Observação"))

    # Data de criação
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))

    def __str__(self):
        return f"{self.get_adjustment_type_display()} - {self.salary.employee.user.full_name} ({self.amount})"
