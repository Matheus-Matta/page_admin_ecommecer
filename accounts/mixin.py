from .models import ActionLog
from django.shortcuts import redirect


class LoggableMixin:
    """
    Mixin genérico para registrar logs automaticamente durante o save().
    """

    def save(self, *args, user=None, action_text=None, **kwargs):
        """
        Sobrescreve o método save para registrar logs de alterações.
        :param user: Instância do usuário que realizou a ação.
        :param action_text: Descrição da ação realizada.
        """
        # Chama o método save padrão para salvar o modelo
        super().save(*args, **kwargs)

        # Registrar o log
        if user and action_text:
            ActionLog.objects.create(
                user=user,
                employee=getattr(self, "employee", None),
                action_text=f"{action_text} - [{self.__class__.__name__}]",
            )


class RedirectAuthenticatedMixin:
    """Mixin que redireciona usuários autenticados para a página principal."""

    redirect_authenticated_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_url)
        return super().dispatch(request, *args, **kwargs)
