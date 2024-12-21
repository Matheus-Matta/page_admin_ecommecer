from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from .mixin import RedirectAuthenticatedMixin


# Login Page View
class LoginPageView(RedirectAuthenticatedMixin, View):
    template_name = "auth/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        next_url = request.GET.get("next", "/")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email or not password:
            messages.error(request, "Dados de login não fornecidos")
        else:
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
            else:
                messages.error(request, "Email ou Senha incorretos")

        return redirect(next_url)


# Suporte Page View
class SuportePageView(RedirectAuthenticatedMixin, View):
    template_name = "auth/suporte.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def LogoutView(request):
    logout(request)
    return redirect("login")
