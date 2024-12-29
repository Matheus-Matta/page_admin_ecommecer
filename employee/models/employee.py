from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin
from accounts.models.user import User
from .role import Role
from .permission import Permission
from .contract_type import ContractType
from .document import Document
from .paymentDetails import PaymentDetails
from .salary import Salary
from accounts.models.address import Address

from .actions import *


# Modelo de Funcionário
class Employee(LoggableMixin, models.Model):

    # Relaciona o funcionário a um usuário do sistema
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee",
        verbose_name=_("Usuário"),
        blank=True,
        null=True,
    )

    email = models.EmailField(
        max_length=255,
        verbose_name=_("E-mail"),
        blank=False,
        null=False,
    )

    # Adicionando um campo personalizado
    full_name = models.CharField(
        max_length=255, verbose_name=_("Nome Completo"), blank=True, null=True
    )

    # Data de nascimento do funcionário
    birth_date = models.DateField(verbose_name=_("Data de Nascimento"))

    # CPF único do funcionário
    cpf = models.CharField(max_length=14, unique=True, verbose_name=_("CPF"))

    # RG ou outro documento de identificação
    rg = models.CharField(
        max_length=20, verbose_name=_("RG ou Outro Documento de Identificação")
    )

    # Carteira de Trabalho e Previdência Social
    ctps = models.CharField(
        max_length=20, verbose_name=_("CTPS"), blank=True, null=True
    )

    # Número do PIS/PASEP
    pis_pasep = models.CharField(
        max_length=20, verbose_name=_("PIS/PASEP"), blank=True, null=True
    )

    # CNH do funcionário (opcional)
    cnh = models.CharField(max_length=20, verbose_name=_("CNH"), blank=True, null=True)

    # Telefone de contato do funcionário
    phone = models.CharField(max_length=15, verbose_name=_("Telefone"))

    # Data de admissão (preenchida automaticamente)
    hire_date = models.DateField(auto_now_add=True, verbose_name=_("Data de Admissão"))

    # Data de desligamento (se aplicável)
    termination_date = models.DateField(
        blank=True, null=True, verbose_name=_("Data de Desligamento")
    )

    # Horário de início do trabalho
    start_time = models.TimeField(verbose_name=_("Horário de Início"))

    # Horário de término do trabalho
    end_time = models.TimeField(verbose_name=_("Horário de Término"))

    # Gênero do funcionário
    gender = models.CharField(
        max_length=10,
        choices=[("M", "Masculino"), ("F", "Feminino")],
        verbose_name=_("Gênero"),
    )

    # Situação atual do funcionário na empresa
    employment_status = models.CharField(
        max_length=15,
        choices=[
            ("active", "Ativo"),
            ("on_advanve", "De Férias"),
            ("on_leave", "De Licença"),
            ("terminated", "Demitido"),
        ],
        verbose_name=_("Status de Emprego"),
    )

    # tipo de contrato
    contractType = models.ForeignKey(
        ContractType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ContractType",
        verbose_name=_("Tipo de contrato"),
    )

    # Cargo do funcionário
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        related_name="employees",
        verbose_name=_("Cargo"),
    )

    # Relaciona documentos ao funcionário
    documents = models.ManyToManyField(
        Document,
        null=True,
        related_name="documents",
        verbose_name=_("Employee"),
    )

    # Relaciona os detalhes de pagamento ao funcionário
    payment_details = models.ForeignKey(
        PaymentDetails,
        on_delete=models.CASCADE,
        null=True,
        related_name="payment_details",
        verbose_name=_("Employee"),
    )

    # Relaciona o salário ao funcionário
    salary = models.ForeignKey(
        Salary,
        on_delete=models.CASCADE,
        null=True,
        related_name="salaries",
        verbose_name=_("Funcionário"),
    )

    # Permissões associadas ao cargo
    permissions = models.ManyToManyField(
        Permission, related_name="roles", verbose_name=_("Permissions")
    )

    # Endereços associados ao funcionário
    address = models.ManyToManyField(
        Address, related_name="addresses", verbose_name=_("endereços de Funcionários")
    )

    def save(self, *args, **kwargs):
        """
        Salva o funcionário e atribui as permissões do cargo, se aplicável.
        """
        super().save(*args, **kwargs)
        if self.role:
            self.permissions.set(self.role.permissions.all())

    def __str__(self):
        return self.user.full_name

    def display_name(self):
        """
        Retorna apenas o primeiro e o segundo nome do funcionário.
        """
        if not self.full_name:
            return ""

        # Divide o nome completo em partes
        name_parts = self.full_name.split()

        # Retorna apenas o primeiro e o segundo nome
        return " ".join(name_parts[:2])

    @classmethod
    def create_user(cls, data):
        """
        Criar um funcionario com todos os dados
        """
        # server para que todas dados sejam criados caso tenha algum erro ela revoga os dados anteriores
        with transaction.atomic():  # Inicia a transação
            try:
                action_validate_data_user(cls, data)
                return action_create_employee_user(cls, data)
            except ValidationError as e:
                # Trate validações específicas
                raise e
            except Exception as e:
                # Trate outras exceções
                raise Exception(f"Erro ao criar usuário: {e}")

    def calculate_salary(self):
        """
        Calcula o salário líquido com base no salário bruto, descontos e bônus associados.
        """
        return action_calculate_salary(self)

    def get_salary_discounts(self):
        """
        Retorna uma lista detalhada de descontos aplicados.
        """
        return action_get_salary_disconts(self)

    def calculate_adjustments(self, start_date=None, end_date=None):
        """
        calcula o ajuste de salario com base em ( faltas , vales, ou comissoes)
        """
        return action_calculate_adjustments(self, start_date, end_date)

    def get_salary_summary(self, start_date=None, end_date=None):
        """
        busca e retorna os dados de folha de salario
        """
        return action_get_salary_summary(self, start_date, end_date)

    def has_permission(self, permission_name):
        """
        verifica se o funcionario possui a permissao
        """
        return action_has_permission(self, permission_name)
