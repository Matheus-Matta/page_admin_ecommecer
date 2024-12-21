from .models import User
from django.db.models.signals import post_migrate
from decouple import config


def create_superuser(sender, **kwargs):
    """Cria um superusuário padrão ao executar 'migrate'."""
    superuser_email = config("DEFAULT_USER_EMAIL", default="admin@admin.com")
    superuser_password = config("DEFAULT_USER_PASSWORD", default="admin123")

    if superuser_email and superuser_password:
        if not User.objects.filter(username=superuser_email).exists():
            User.objects.create_superuser(
                username=superuser_email,
                email=superuser_email,
                password=superuser_password,
            )
            print(
                f"Superuser '{superuser_email}' '{superuser_password}' created successfully."
            )


post_migrate.connect(create_superuser)
