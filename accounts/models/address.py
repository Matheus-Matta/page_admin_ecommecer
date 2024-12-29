from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin


# Modelo de Endereço
class Address(LoggableMixin, models.Model):
   
    # Rua do endereço
    street = models.CharField(max_length=255, verbose_name=_("Street"))

    # Número do endereço
    number = models.CharField(max_length=10, verbose_name=_("Number"))

    # Complemento do endereço (opcional)
    complement = models.CharField(
        max_length=255, verbose_name=_("Complement"), blank=True, null=True
    )

    # Bairro do endereço
    neighborhood = models.CharField(max_length=100, verbose_name=_("Neighborhood"))

    # Cidade do endereço
    city = models.CharField(max_length=100, verbose_name=_("City"))

    # Estado do endereço
    state = models.CharField(max_length=100, verbose_name=_("State"))

    # País do endereço
    country = models.CharField(max_length=100, verbose_name=_("Country"))

    # Código postal do endereço
    postal_code = models.CharField(max_length=20, verbose_name=_("Postal Code"))

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}, {self.state}"
