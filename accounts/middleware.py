from django.utils.timezone import now
from .models.actionLog import ActionLog
from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from django.contrib.sessions.models import Session


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


class ResetSessionTimeoutMiddleware:
    """
    Middleware que reseta o tempo de expiração da sessão se o usuário estiver ativo.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se o usuário está autenticado
        if request.user.is_authenticated:
            # Recupera a última atividade
            last_activity = request.session.get("last_activity")

            if last_activity:
                # Calcula o tempo desde a última atividade
                elapsed_time = now() - last_activity

                # Verifica se o tempo de inatividade excede o permitido
                if elapsed_time.total_seconds() > settings.SESSION_COOKIE_AGE:
                    # Finaliza a sessão
                    request.session.flush()
                else:
                    # Atualiza o tempo da última atividade
                    request.session["last_activity"] = now()
            else:
                # Define a última atividade na primeira requisição
                request.session["last_activity"] = now()

        response = self.get_response(request)
        return response
