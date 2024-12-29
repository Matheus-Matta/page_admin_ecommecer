from django.utils.timezone import now
from .models.actionLog import ActionLog
from django.utils.timezone import now
from .signals import log_user_session
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
from django.shortcuts import redirect
from .models.UserSessionLog import UserSessionLog


class ActionLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Antes de processar a view
        response = self.get_response(request)

        # Após processar a view
        if request.user.is_authenticated:  # Apenas logar ações de usuários autenticados
            status_code = response.status_code

            # Salva apenas se o status for diferente de 200 e 201
            if status_code not in [200, 201]:
                if request.method != "GET":
                    action_text = (
                        f"Erro - URL: {request.path}, Método: {request.method}"
                    )

                    # Registrar o log
                    ActionLog.objects.create(
                        user=request.user,
                        action_text=action_text,
                        status_code=status_code,
                        action_date=now(),
                    )

        return response


class SessionExpirationMiddleware:
    """
    Middleware para gerenciar sessões personalizadas.
    Verifica se a sessão expirou e, caso o usuário esteja ativo, reinicia o tempo de expiração.
    """

    SESSION_TIMEOUT = getattr(
        settings, "CUSTOM_SESSION_TIMEOUT", 3600
    )  # 1 hora por padrão

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get("last_activity")

            if last_activity:
                from datetime import datetime

                last_activity_time = datetime.fromisoformat(last_activity)
                elapsed_time = now() - last_activity_time

                if elapsed_time.total_seconds() > settings.CUSTOM_SESSION_TIMEOUT:
                    log_user_session(request, UserSessionLog.ActionChoices.EXPIRED)
                    request.session.flush()
                    return redirect("login")

            request.session["last_activity"] = now().isoformat()

        return self.get_response(request)
