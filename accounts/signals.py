from django.db import connection
from django.db.models.signals import post_migrate
from decouple import config
from django.contrib.auth import get_user_model
from .models.UserSessionLog import UserSessionLog
import requests
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserSessionLog
from django.utils.timezone import now


def table_exists(table_name):
    """
    Verifica se uma tabela existe no banco de dados.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=%s",
            [table_name],
        )
        return cursor.fetchone() is not None


def create_or_get_superuser():
    """
    Cria ou recupera o superusuário padrão.
    """
    if not table_exists("accounts_user"):
        print("A tabela 'accounts_user' ainda não foi criada. Ignorando.")
        return None

    User = get_user_model()
    default_email = config("DEFAULT_USER_EMAIL")
    default_password = config("DEFAULT_USER_PASSWORD")
    default_username = config("DEFAULT_USER_USERNAME", default="admin")

    if not default_email or not default_password:
        raise ValueError(
            "DEFAULT_USER_EMAIL e DEFAULT_USER_PASSWORD precisam estar configurados."
        )

    user, created = User.objects.get_or_create(
        username=default_username,
        email=default_email,
        defaults={
            "is_staff": True,
            "is_superuser": True,
        },
    )

    if created:
        user.set_password(default_password)
        user.save()
        print(f"O superusuário '{user.username}' foi criado.")

    return user


def get_or_create_default_superuser(sender, **kwargs):
    """
    Sinal para criar ou recuperar o superusuário após as migrações.
    """
    create_or_get_superuser()


post_migrate.connect(get_or_create_default_superuser)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    request.session["last_activity"] = now().isoformat()
    log_user_session(request, UserSessionLog.ActionChoices.LOGIN)


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    log_user_session(request, UserSessionLog.ActionChoices.LOGOUT)


def get_client_ip_and_location(request):
    """
    Obtém o IP do cliente e localiza sua posição geográfica usando ipinfo.io.
    """
    try:
        # Verifica o cabeçalho HTTP_X_FORWARDED_FOR
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            # Se não houver, usa o REMOTE_ADDR como fallback
            ip = request.META.get("REMOTE_ADDR", "127.0.0.1")

        # Ignorar IPs locais
        if ip in ("127.0.0.1", "localhost"):
            return ip, {}

        # Requisição para obter informações de localização
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            location_info = {
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "latitude": data.get("loc", "").split(",")[0],
                "longitude": data.get("loc", "").split(",")[1],
                "isp": data.get("org"),
            }
            return ip, location_info
    except Exception as e:
        print(f"Erro ao obter a localização: {e}")

    return "0.0.0.0", {}


def log_user_session(request, action):
    """
    Registra um log de sessão para o usuário.
    """
    if request.user.is_anonymous:  # Ignora usuários anônimos
        return

    ip, location_info = get_client_ip_and_location(request)

    UserSessionLog.objects.create(
        user=request.user,
        ip_address=ip,
        action=action,
        city=location_info.get("city"),
        region=location_info.get("region"),
        country=location_info.get("country"),
        latitude=location_info.get("latitude"),
        longitude=location_info.get("longitude"),
        isp=location_info.get("isp"),
    )
