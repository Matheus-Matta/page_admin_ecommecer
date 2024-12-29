from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin
from .employee import Employee


# Modelo para registrar treinamentos realizados pelo funcionário
class Training(LoggableMixin, models.Model):
    # Relaciona o treinamento ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="trainings"
    )
    # Nome do treinamento
    training_name = models.CharField(
        max_length=255, verbose_name=_("Nome do Treinamento")
    )
    # Provedor ou instituição responsável pelo treinamento
    provider = models.CharField(max_length=255, verbose_name=_("Provedor"))
    # Data de início do treinamento
    start_date = models.DateField(verbose_name=_("Data de Início"))
    # Data de término do treinamento
    end_date = models.DateField(verbose_name=_("Data de Fim"))
    # Certificado emitido após o treinamento (opcional)
    certificate = models.FileField(
        upload_to="employee_trainings/",
        verbose_name=_("Certificado"),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Treinamento de {self.employee.user.full_name} - {self.training_name}"


# Modelo para registrar avaliações de desempenho
class PerformanceReview(LoggableMixin, models.Model):
    # Relaciona a avaliação ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="performance_reviews"
    )
    # Data da avaliação
    review_date = models.DateField(verbose_name=_("Data da Avaliação"))
    # Pontuação da avaliação
    score = models.IntegerField(
        verbose_name=_("Pontuação"),
        choices=[
            (1, "Ruim"),
            (2, "Regular"),
            (3, "Bom"),
            (4, "Muito Bom"),
            (5, "Excelente"),
        ],
    )
    # Comentários adicionais sobre a avaliação (opcional)
    comments = models.TextField(verbose_name=_("Comentários"), blank=True, null=True)

    def __str__(self):
        return f"Avaliação de {self.employee.user.full_name} em {self.review_date}"
