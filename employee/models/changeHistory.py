from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin
from .employee import Employee


# Modelo para registrar histórico de alterações nos dados do funcionário
class DataChangeHistory(LoggableMixin, models.Model):
    # Relaciona a alteração ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="data_changes"
    )
    # Nome do campo alterado
    field_name = models.CharField(max_length=255, verbose_name=_("Campo Alterado"))
    # Valor antigo do campo
    old_value = models.TextField(verbose_name=_("Valor Antigo"))
    # Novo valor do campo
    new_value = models.TextField(verbose_name=_("Novo Valor"))
    # Data e hora da alteração
    change_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Data da Alteração")
    )

    def __str__(self):
        return f"Alteração de dados para {self.employee.user.full_name} em {self.change_date}"
