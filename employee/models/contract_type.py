from django.db import models
from accounts.mixin import LoggableMixin
from django.utils.translation import gettext_lazy as _


class SalaryDiscount(LoggableMixin, models.Model):
    """
    Modelo principal de descontos salariais, ex.: INSS, IRRF.
    """

    name = models.CharField(max_length=250, verbose_name=_("Nome do Desconto"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))

    def __str__(self):
        return self.name


class DiscountBracket(LoggableMixin, models.Model):
    """
    Faixas de desconto associadas a um desconto principal (ex.: INSS).
    """

    salary_discount = models.ForeignKey(
        SalaryDiscount,
        on_delete=models.CASCADE,
        related_name="brackets",
        verbose_name=_("Desconto Salarial"),
    )

    min_value = models.DecimalField(
        max_digits=10,
        null=True,
        blank=True,
        decimal_places=2,
        verbose_name=_("Valor Mínimo"),
    )

    max_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Valor Máximo"),
        null=True,
        blank=True,
    )

    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Porcentagem de Desconto")
    )

    def __str__(self):
        max_str = f"{self.max_value}" if self.max_value else "Acima"
        return f"{self.min_value} - {max_str} ({self.percentage}%)"


# Modelo de Cargo
class ContractType(LoggableMixin, models.Model):
    # Nome do cargo
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    discounts = models.ManyToManyField(
        SalaryDiscount,
        related_name="contract_types",
        verbose_name=_("Descontos Associados"),
    )

    def __str__(self):
        return self.name
