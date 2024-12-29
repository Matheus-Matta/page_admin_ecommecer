from accounts.models.user import User
from accounts.models.address import Address

from employee.models.document import Document
from employee.models.paymentDetails import PaymentDetails
from employee.models.salary import Salary
from datetime import datetime


def action_create_employee_user(cls, data):
    """
    Cria um funcionário com base nos dados fornecidos no formulário.
    A função é executada dentro de uma transação atômica.
    """

    request_user = data["request_user"]  # user que requisitou

    # Criação do usuário
    user = User.objects.create_user(
        username=data["user_email"].split("@")[0],
        email=data["user_email"],
        password=data["user_pass"],
    )
    user.log(request_user, f"Criou o usuário {user.email}", 201)

    # Criação de detalhes de pagamento
    payment_details = PaymentDetails.objects.create(
        payment_type=data["payment_type"],
        payment_method_id=data["payment_method"],
        pix_key=data.get("pix_key"),
        bank_name=data.get("bank_name"),
        account_number=data.get("account_number"),
        agency_number=data.get("agency_number"),
    )

    payment_details.log(
        request_user, f"Criou os detalhes de pagamento para {data["name"]}", 201
    )

    # Criação do salário
    salary = Salary.objects.create(
        start_date=data["start_date"],
        end_date=data["end_date"] if data["end_date"] else None,
        gross_salary=gross_salary_to_float(data["gross_salary"]),
    )
    salary.log(request_user, f"Criou o salário para {data["name"]}", 201)

    # Criação do funcionário
    employee = cls.objects.create(
        user=user,
        full_name=data["name"],
        email=data["email"],
        birth_date=datetime.strptime(data["birth_date"], "%d/%m/%Y").date(),
        cpf=data["cpf"],
        rg=data["rg"],
        ctps=data["ctps"],
        pis_pasep=data["pis_pasep"],
        cnh=data["cnh"],
        phone=data["phone"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        employment_status="active",
        contractType_id=data["contract_type"],
        role_id=data["role"],
        payment_details=payment_details,
        salary=salary,
    )

    employee.log(request_user, f"Criou o funcionário {employee.full_name}", 201)

    # Criação de documentos
    if "documents" in data:
        document = Document.save_files(
            request_user, "Documentos do funcionário", data["documents"]
        )
        # Associa os documentos ao funcionário
        employee.documents.add(document)
        document.log(
            request_user,
            f"Criou o documento '{document.description}' para {employee.full_name}",
            201,
        )
    i = 0
    while f"addresses[{i}][street]" in data:
        address = Address.objects.create(
            street=data.get(f"addresses[{i}][street]"),
            number=data.get(f"addresses[{i}][number]"),
            complement=data.get(f"addresses[{i}][complement]", ""),
            neighborhood=data.get(f"addresses[{i}][neighborhood]"),
            city=data.get(f"addresses[{i}][city]"),
            state=data.get(f"addresses[{i}][state]"),
            country=data.get(f"addresses[{i}][country]"),
            postal_code=data.get(f"addresses[{i}][postal_code]"),
        )
        i += 1
        employee.address.add(address)
        address.log(request_user, f"Criou o endereço {address}", 201)

    return employee


def gross_salary_to_float(value):
    """
    Converte uma string formatada como "R$ 1.500,00" em um número decimal.
    """
    if isinstance(value, str):
        value = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
    return float(value)  # Ou Decimal(value) para maior precisão


def parse_addresses(data):
    """
    Reconstrói os endereços a partir do QueryDict.
    """
