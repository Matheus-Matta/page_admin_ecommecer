from django.db import connection
from django.db.models.signals import post_migrate
from decouple import config
from django.contrib.auth import get_user_model


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
