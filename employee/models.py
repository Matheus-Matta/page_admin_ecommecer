from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from accounts.mixin import LoggableMixin


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
            ("on_leave", "De Férias"),
            ("terminated", "Demitido"),
        ],
        verbose_name=_("Status de Emprego"),
    )
    # Tipo de contrato do funcionário
    contract_type = models.CharField(
        max_length=15,
        choices=[
            ("clt", "CLT"),
            ("pj", "PJ"),
            ("internship", "Estágio"),
            ("apprentice", "Jovem Aprendiz"),
        ],
        verbose_name=_("Tipo de Contrato"),
    )
    # Método de pagamento (mensal ou quinzenal)
    payment_method = models.CharField(
        max_length=10,
        choices=[("monthly", "Mensal"), ("biweekly", "Quinzenal")],
        verbose_name=_("Forma de Pagamento"),
    )
    # Cargo do funcionário
    role = models.ForeignKey(
        "Role",
        on_delete=models.SET_NULL,
        null=True,
        related_name="employees",
        verbose_name=_("Cargo"),
    )

    def __str__(self):
        return self.user.full_name


# Modelo de Salários
class Salary(LoggableMixin, models.Model):
    # Relaciona o salário ao funcionário
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salaries",
        verbose_name=_("Funcionário"),
    )
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
    # Valor líquido do salário após descontos
    net_salary = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Salário Líquido")
    )
    # Benefícios oferecidos pela empresa (ex.: vale-transporte, alimentação)
    benefits = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Benefícios"),
    )
    # Valor de bônus ou gratificações adicionais (opcional)
    bonus = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Bônus")
    )
    # Desconto do INSS
    inss_discount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Desconto INSS")
    )
    # Desconto do IRRF
    irrf_discount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Desconto IRRF")
    )
    # Valor do vale-transporte descontado
    transport_voucher = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Vale-Transporte"),
    )

    def __str__(self):
        return f"Salário de {self.employee.user.full_name} ({self.start_date} - {self.end_date if self.end_date else 'Atual'})"


# Modelo de Descontos no Salário
class SalaryDiscount(LoggableMixin, models.Model):
    # Funcionário relacionado ao desconto
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salary_discounts",
        verbose_name=_("Employee"),
    )
    # Tipo de desconto aplicado
    discount_type = models.CharField(max_length=50, verbose_name=_("Discount Type"))
    # Valor do desconto
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Amount")
    )
    # Data em que o desconto foi aplicado
    date = models.DateField(verbose_name=_("Date"))
    # Observação sobre o desconto
    observation = models.TextField(blank=True, null=True, verbose_name=_("Observation"))

    def __str__(self):
        return f"Discount for {self.employee.user.full_name}"


# Modelo de Endereço
class Address(LoggableMixin, models.Model):
    # Endereços associados ao funcionário
    employees = models.ManyToManyField(
        "Employee", related_name="addresses", verbose_name=_("Funcionários")
    )
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


# Modelo de Detalhes de Pagamento
class PaymentDetails(LoggableMixin, models.Model):
    # Relaciona os detalhes de pagamento ao funcionário
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="payment_details",
        verbose_name=_("Employee"),
    )
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
        max_length=255, blank=True, null=True, verbose_name=_("PIX Key")
    )
    # Nome do banco
    bank_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Bank Name")
    )
    # Número da conta bancária
    account_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Account Number")
    )
    # Número da agência bancária
    agency_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Agency Number")
    )

    def __str__(self):
        return f"Payment Details for {self.employee.user.full_name}"


# Modelo de Cargo
class Role(LoggableMixin, models.Model):
    # Nome do cargo
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    # Abreviação do cargo
    abbreviation = models.CharField(max_length=10, verbose_name=_("Abbreviation"))
    # Permissões associadas ao cargo
    permissions = models.ManyToManyField(
        "Permission", related_name="roles", verbose_name=_("Permissions")
    )

    def __str__(self):
        return self.name


# Modelo de Permissão
class Permission(LoggableMixin, models.Model):
    # Nome da permissão
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        
        return self.name


# Modelo de Documentos
class Document(LoggableMixin, models.Model):
    # Relaciona documentos ao funcionário
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Employee"),
    )
    # Arquivos associados ao documento
    files = models.ManyToManyField(
        "UploadedFile", related_name="documents", verbose_name=_("Files")
    )
    # Descrição do documento
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    # Data de upload do documento
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    def __str__(self):
        return f"{self.description} - {self.employee.user.full_name}"


# Modelo para Arquivos Enviados
class UploadedFile(LoggableMixin, models.Model):
    # Arquivo enviado
    file = models.FileField(upload_to="uploads/", verbose_name=_("File"))
    # Nome do arquivo (opcional, pode ser preenchido automaticamente)
    name = models.CharField(
        max_length=255, verbose_name=_("File Name"), blank=True, null=True
    )
    # Data de upload
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    def save(self, *args, **kwargs):
        # Preenche o nome automaticamente, se não for fornecido
        if not self.name:
            self.name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Modelo para registrar adiantamentos feitos ao funcionário
class Advance(LoggableMixin, models.Model):
    # Relaciona o adiantamento ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="advances"
    )
    # Valor do adiantamento
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Valor")
    )
    # Data em que o adiantamento foi realizado
    date = models.DateField(verbose_name=_("Data"))
    # Descrição opcional do adiantamento
    description = models.CharField(
        max_length=255, verbose_name=_("Descrição"), blank=True, null=True
    )

    def __str__(self):
        return f"Adiantamento para {self.employee.user.full_name} - {self.amount}"


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
    # Número de dias de férias utilizados
    days_taken = models.PositiveIntegerField(verbose_name=_("Dias Usados"))
    # Status das férias (aprovado ou pendente)
    status = models.CharField(
        max_length=10,
        choices=[("approved", "Aprovado"), ("pending", "Pendente")],
        verbose_name=_("Status"),
    )

    def __str__(self):
        return f"Férias de {self.employee.user.full_name} ({self.start_date} a {self.end_date})"


# Modelo para registrar licenças do funcionário
class Leave(LoggableMixin, models.Model):
    # Relaciona a licença ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="leaves"
    )
    # Tipo de licença (ex.: médica ou pessoal)
    leave_type = models.CharField(
        max_length=50,
        choices=[("sick", "Licença Médica"), ("personal", "Licença Pessoal")],
        verbose_name=_("Tipo de Licença"),
    )
    # Data de início da licença
    start_date = models.DateField(verbose_name=_("Data de Início"))
    # Data de término da licença
    end_date = models.DateField(verbose_name=_("Data de Fim"))
    # Status da licença (aprovada ou pendente)
    status = models.CharField(
        max_length=10,
        choices=[("approved", "Aprovado"), ("pending", "Pendente")],
        verbose_name=_("Status"),
    )

    def __str__(self):
        return f"Licença de {self.employee.user.full_name} ({self.start_date} a {self.end_date})"


# Modelo para registrar ausências do funcionário
class Absence(LoggableMixin, models.Model):
    # Relaciona a ausência ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="absences"
    )
    # Data da ausência
    absence_date = models.DateField(verbose_name=_("Data da Ausência"))
    # Motivo da ausência (opcional)
    reason = models.CharField(
        max_length=255, verbose_name=_("Motivo"), blank=True, null=True
    )
    # Status da ausência (justificada ou não justificada)
    status = models.CharField(
        max_length=10,
        choices=[("excused", "Justificada"), ("unexcused", "Não Justificada")],
        verbose_name=_("Status"),
    )

    def __str__(self):
        return f"Ausência de {self.employee.user.full_name} em {self.absence_date}"


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


# Modelo conquistas predefinidas
class Achievement(LoggableMixin, models.Model):
    # Conquista pode estar associada a vários funcionários
    employees = models.ManyToManyField(
        "Employee", related_name="achievements", verbose_name=_("Funcionários")
    )
    # Nome da conquista
    name = models.CharField(max_length=255, verbose_name=_("Nome da Conquista"))
    # Imagem associada à conquista
    image = models.ImageField(
        upload_to="employee_achievements/", verbose_name=_("Imagem da Conquista")
    )

    def __str__(self):
        return f"Conquista: {self.name}"
