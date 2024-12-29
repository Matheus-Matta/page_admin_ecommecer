from django.urls import path
from .views import *

urlpatterns = [
    path("view/", EmployeePageView.as_view(), name="funcionarios"),
    path("list/", EmployeeGetList.as_view(), name="lista_funcionarios"),
]
