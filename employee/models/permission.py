from django.db import models
from accounts.mixin import LoggableMixin
from django.utils.translation import gettext_lazy as _


# Modelo de Permissão
class Permission(LoggableMixin, models.Model):
    # Nome da permissão
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    # Permissão pai (auto-referenciada)
    parent = models.ForeignKey(
        "self",  # Referencia a própria model
        on_delete=models.CASCADE,  # Define o comportamento ao excluir
        related_name="sub_permissions",  # Nome do relacionamento reverso
        blank=True,
        null=True,  # Permissões sem pai são as principais
        verbose_name=_("Parent Permission"),
    )

    def __str__(self):
        return f"{self.name} ({'Sub' if self.parent else 'Main'})"

    @classmethod
    def get_structure(cls):
        """
        Retorna as permissões em uma estrutura hierárquica.
        
        exemplo de retorno:
        
            "E-commerce": {
                "Pedidos": ["Ver", "Editar", "Criar"],
            },
            "Funcionários": {
                "Cargos": ["Ver", "Editar", "Criar"],
            },
        
        """
        # Obter todas as permissões principais (sem pai)
        main_permissions = cls.objects.filter(parent__isnull=True).prefetch_related(
            "sub_permissions"
        )

        structure = {}
        for main_permission in main_permissions:
            structure[main_permission.name] = {}

            # Iterar pelas permissões filhas (subcategorias)
            for sub_permission in main_permission.sub_permissions.all():
                structure[main_permission.name][sub_permission.name] = []

                # Iterar pelas a es dentro da subcategoria
                for action in sub_permission.sub_permissions.all():
                    structure[main_permission.name][sub_permission.name].append(
                        action.name.rsplit(" (", 1)[-1].rstrip(")")
                    )

        return structure
