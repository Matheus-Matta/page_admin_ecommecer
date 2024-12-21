from django.urls import path
from .views import *

urlpatterns = [
    # authenticate urls
    path("login/", LoginPageView.as_view(), name="login"),  # render page login
    path("suporte/", SuportePageView.as_view(), name="suporte"),  # render page suporte
    path("logout/", LogoutView, name="logout"),  # logout url
]
