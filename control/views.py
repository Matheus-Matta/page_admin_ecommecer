from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# Simulação de banco de dados em memória
saved_content = {"content": None}


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    login_url = (
        "accounts/login/"  # URL para redirecionar caso o usuário não esteja logado
    )
    redirect_field_name = "next"  # Campo para armazenar a URL original

    def get_context_data(self, **kwargs):
        """Adiciona o conteúdo salvo ao contexto."""
        context = super().get_context_data(**kwargs)
        context["content"] = saved_content["content"]  # Adiciona o conteúdo salvo
        return context

    @method_decorator(csrf_exempt)  # Permite requisições POST sem CSRF para salvar
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Recebe e salva o conteúdo do editor."""
        if request.method == "POST":
            data = json.loads(request.body)
            saved_content["content"] = data.get("content", "")
            return JsonResponse({"message": "Conteúdo salvo com sucesso."})
        return JsonResponse({"error": "Método não permitido."}, status=405)
