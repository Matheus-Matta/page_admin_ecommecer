from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from .models.role import Role
from .models.contract_type import ContractType
from .models.paymentDetails import PaymentMethod
from .models.employee import Employee
from .utils.format_last_login import format_last_login
from datetime import datetime
import locale


class EmployeePageView(LoginRequiredMixin, View):
    template_name = "pages/funcionario.html"
    login_url = "accounts/login/"
    redirect_field_name = "next"

    def get(self, request, *args, **kwargs):

        # Buscar dados de cargos (Roles) e tipos de contrato (ContractType)
        roles = Role.objects.all()
        contract_types = ContractType.objects.all()
        payment_methods = PaymentMethod.objects.all()

        # Passar os dados para o contexto do template
        context = {
            "roles": roles,
            "contract_types": contract_types,
            "payment_methods": payment_methods,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            form_data = request.POST.dict()
            form_data["documents"] = request.FILES.getlist("documents")
            form_data["request_user"] = request.user
            employee = Employee.create_user(form_data)
            return JsonResponse(
                {
                    "success": True,
                    "message": "Funcionário criado com sucesso!",
                },
                status=201,
            )
        except Exception as e:
            print(f"Erro: {e}")
            return JsonResponse(
                {"success": False, "message": str(e)},
                status=400,
            )


class EmployeeGetList(LoginRequiredMixin, View):
    login_url = "accounts/login/"
    redirect_field_name = "next"

    def get(self, request, *args, **kwargs):
        page_size = int(request.GET.get("length", 10))  # Número de registros por página
        start = int(request.GET.get("start", 0))  # Índice inicial
        page_number = start // page_size + 1  # Página atual
        search_value = request.GET.get("search[value]", "")  # Texto de busca
        order_column_index = int(
            request.GET.get("order[0][column]", 0)
        )  # Coluna ordenada
        order_dir = request.GET.get("order[0][dir]", "asc")  # Direção da ordenação
        roles = request.GET.getlist("roles[]")  # Filtro de cargos
        status = request.GET.getlist("status[]")  # Filtro de s
        start_date = request.GET.get("start_date")  # Data inicial
        end_date = request.GET.get("end_date")  # Data
        export = request.GET.get("export", False)  # Checa se é uma exportação
        print(export)
        # Mapeando colunas para ordenação com base no índice do DataTables
        columns = [
            "full_name",
            "role__name",
            "user__last_login",
            "employment_status",
            "user__date_joined",
        ]
        order_column = columns[order_column_index]

        # Ajusta direção da ordenação
        if order_dir == "desc":
            order_column = f"-{order_column}"

        # Base query
        queryset = Employee.objects.select_related("role", "user").all()

        # Verifica se os filtros são aplicáveis apenas se contiverem valores
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%d/%m/%Y")
                end_date = datetime.strptime(end_date, "%d/%m/%Y")
                queryset = queryset.filter(
                    user__date_joined__range=(start_date, end_date)
                )
            except ValueError:
                pass  # Ignora o filtro caso as datas estejam inválidas

        if roles and any(roles):  # Verifica se há IDs válidos
            queryset = queryset.filter(role_id__in=[role for role in roles if role])

        if status and any(status):  # Verifica se há status válidos
            queryset = queryset.filter(employment_status__in=status)

        # Aplicar filtro de busca
        if search_value:
            queryset = queryset.filter(
                Q(full_name__icontains=search_value)
                | Q(email__icontains=search_value)
                | Q(role__name__icontains=search_value)
            )

        # Ordenação
        queryset = queryset.order_by(order_column)

        # Se export=True, ignora a paginação
        if export:
            # Ignora paginação e retorna todos os dados filtrados
            data = [
                {
                    "user": {
                        "id": employee.id,
                        "email": employee.user.email,
                        "name": employee.display_name(),
                    },
                    "role": employee.role.name if employee.role else "Sem Cargo",
                    "last_login": (
                        format_last_login(
                            employee.user.last_login.strftime("%Y-%m-%dT%H:%M:%S")
                        )
                        if employee.user.last_login
                        else "Nunca"
                    ),
                    "situacao": employee.employment_status,
                    "joined_date": dataformat(
                        employee.user.date_joined.strftime("%Y-%m-%dT%H:%M:%S")
                    ),
                }
                for employee in queryset
            ]
            print("page ignorada")
            return JsonResponse({"data": data}, status=200)

        # Paginação
        paginator = Paginator(queryset, page_size)
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = []

        # Serializar os dados para o DataTables
        data = [
            {
                "user": {
                    "id": employee.id,
                    "email": employee.user.email,
                    "name": employee.display_name(),
                },
                "role": employee.role.name if employee.role else "Sem Cargo",
                "last_login": (
                    format_last_login(
                        employee.user.last_login.strftime("%Y-%m-%dT%H:%M:%S")
                    )
                    if employee.user.last_login
                    else "Nunca"
                ),
                "situacao": employee.employment_status,
                "joined_date": dataformat(
                    employee.user.date_joined.strftime("%Y-%m-%dT%H:%M:%S")
                ),
            }
            for employee in page
        ]

        # Retorno no formato esperado pelo DataTables
        response = {
            "draw": int(request.GET.get("draw", 1)),
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }
        return JsonResponse(response)


def dataformat(value):
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
    # Data no formato original
    data_original = value
    # Converter a string para um objeto datetime
    data_obj = datetime.strptime(data_original, "%Y-%m-%dT%H:%M:%S")
    # Formatar a data no formato desejado
    return data_obj.strftime("%d %B %Y")  # Exemplo: "30 abril 2024"
