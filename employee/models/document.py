import os
from datetime import datetime
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin


def upload_to(instance, filename):
    """
    Define o caminho do upload com base no contexto (ex.: username do funcionário) e um nome único.
    """
    username = getattr(instance, "_user", "anonymous")  # Pega o username ou "anonymous"
    unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
    return os.path.join("uploads", username, unique_name)


# Modelo para Documentos
class Document(LoggableMixin, models.Model):
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    def __str__(self):
        return self.description

    @classmethod
    @transaction.atomic
    def save_files(cls, user, description, files):
        """
        Cria um único documento e associa múltiplos arquivos a ele.

        Args:
            description (str): Descrição do documento.
            files (list): Lista de arquivos para upload.

        Returns:
            Document: Instância do documento criado.
        """
        # Criação do documento
        document = cls.objects.create(description=description)

        # Associação dos arquivos ao documento
        for file in files:
            uploaded_file = UploadedFile(file=file, document=document)
            uploaded_file.save(user=user)  # Passa o usuário autenticado

        return document


# Modelo para Arquivos Enviados
class UploadedFile(LoggableMixin, models.Model):
    file = models.FileField(upload_to=upload_to, verbose_name=_("File"))
    name = models.CharField(
        max_length=255, verbose_name=_("File Name"), blank=True, null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="uploaded_files",  # Alterado para refletir melhor o relacionamento
        verbose_name=_("Document"),
    )

    def save(self, *args, user=None, **kwargs):
        # Atribui o usuário dinamicamente para upload_to
        if user:
            self._user = user.username
        if not self.name:
            self.name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)
