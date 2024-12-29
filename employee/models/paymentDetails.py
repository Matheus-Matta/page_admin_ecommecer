from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin


# Modelo de Detalhes de metodo de pagamento
class PaymentMethod(LoggableMixin, models.Model):
    """
    Modelo para armazenar métodos de pagamento.
    """

    name = models.CharField(
        max_length=250, unique=True, verbose_name=_("Nome do Método de Pagamento")
    )

    def __str__(self):
        return self.get_name_display()


# Modelo de Detalhes de Pagamento
class PaymentDetails(LoggableMixin, models.Model):

    # Tipo de pagamento (PIX, depósito, dinheiro, etc.)
    payment_type = models.CharField(
        max_length=10,
        choices=[
            ("pix", "PIX"),
            ("deposit", "Depósito"),
            ("cash", "Dinheiro"),
            ("other", "Outro"),
        ],
        verbose_name=_("Tipo de Pagamento"),
    )

    # Chave PIX (se aplicável)
    pix_key = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Chave pix")
    )

    # Nome do banco
    bank_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Nome do banco")
    )

    # Número da conta bancária
    account_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Numero de conta")
    )

    # Número da agência bancária
    agency_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Numero agencia")
    )

    # Método de pagamento (mensal ou quinzenal)
    payment_method = models.ForeignKey(
        PaymentMethod,  # Referencia a própria model
        on_delete=models.SET_NULL,  # Define o comportamento ao excluir
        related_name="paymentMethod",  # Nome do relacionamento reverso
        blank=True,
        null=True,  # Permissões sem pai são as principais
        verbose_name=_("Metodo de pagamento"),
    )

    def __str__(self):
        return f"Payment Details for {self.employee.user.full_name}"
