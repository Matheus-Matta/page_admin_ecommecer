from django.shortcuts import redirect


class LoggableMixin:
    """
    Mixin genérico para registrar logs automaticamente durante o save().
    """

    def log(self, user, action_text, status_code=None):
        """
        Método genérico para registrar logs de ações realizadas.
        :param user: Instância do usuário que realizou a ação.
        :param action_text: Descrição da ação realizada.
        """
        from .models.actionLog import ActionLog

        ActionLog.objects.create(
            user=user,
            action_text=f"{user.username} - {action_text} - [{self.__class__.__name__}]",
            status_code=status_code,
        )


class RedirectAuthenticatedMixin:
    """Mixin que redireciona usuários autenticados para a página principal."""

    redirect_authenticated_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_url)
        return super().dispatch(request, *args, **kwargs)
