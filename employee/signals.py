from django.db.models.signals import post_migrate
from .models.permission import Permission
from .models.role import Role
from .models.contract_type import ContractType, SalaryDiscount, DiscountBracket
from .models.employee import Employee
from accounts.signals import create_or_get_superuser
from .models.paymentDetails import PaymentMethod


def setup_employee(sender, **kwargs):
    """
    Configura os tipos de contrato padrão após as migrações.
    """
    # Obtém ou cria o superusuário
    USER = create_or_get_superuser()

    # Lista de tipos de contrato padrão
    default_contract_types = ["CLT", "PJ", "Estágio", "Jovem Aprendiz"]

    # Cria os tipos de contrato, caso ainda não existam
    contract_types = {}
    for contract_name in default_contract_types:
        contract, created = ContractType.objects.get_or_create(name=contract_name)
        if created:
            contract.log(USER, f"Criou o tipo de contrato {contract_name}")
            print(f"Tipo de contrato '{contract_name}' criado.")
        contract_types[contract_name] = contract

    # Criar descontos salariais
    salary_discounts = {}
    discounts_data = {
        "INSS": [
            (0, 1320.00, 7.5),
            (1320.01, 2571.29, 9),
            (2571.30, 3856.94, 12),
            (3856.95, None, 14),
        ],
        "IRRF": [
            (0, 1903.98, 0),
            (1903.99, 2826.65, 7.5),
            (2826.66, 3751.05, 15),
            (3751.06, 4664.68, 22.5),
            (4664.69, None, 27.5),
        ],
        "Vale Transporte": [(0, None, 6)],
    }

    for discount_name, brackets in discounts_data.items():
        discount, created = SalaryDiscount.objects.get_or_create(name=discount_name)
        if created:
            discount.log(USER, f"Criou o desconto '{discount_name}'")
            print(f"Desconto '{discount_name}' criado.")
        salary_discounts[discount_name] = discount

        # Adicionar faixas de desconto
        for min_value, max_value, percentage in brackets:
            bracket, created = DiscountBracket.objects.get_or_create(
                salary_discount=discount,
                min_value=min_value,
                max_value=max_value,
                percentage=percentage,
            )
            if created:
                bracket.log(
                    USER,
                    f"Criou faixa de desconto para '{discount_name}': {min_value} - {max_value} ({percentage}%)",
                )
                print(
                    f"Criou faixa de desconto para '{discount_name}': {min_value} - {max_value} ({percentage}%)"
                )

    # Associar descontos ao tipo de contrato CLT
    clt_contract = contract_types.get("CLT")
    existing_clt_discounts = set(clt_contract.discounts.all())
    clt_discounts_to_add = [
        salary_discounts["INSS"],
        salary_discounts["IRRF"],
        salary_discounts["Vale Transporte"],
    ]

    for discount in clt_discounts_to_add:
        if discount not in existing_clt_discounts:
            clt_contract.discounts.add(discount)
            clt_contract.log(
                USER,
                f"Associou o desconto '{discount.name}' ao contrato CLT",
            )
            print(f"Desconto '{discount.name}' associado ao contrato CLT.")

    # Associar descontos ao tipo de contrato Jovem Aprendiz
    jovem_aprendiz_contract = contract_types.get("Jovem Aprendiz")
    existing_jovem_aprendiz_discounts = set(jovem_aprendiz_contract.discounts.all())
    jovem_aprendiz_discounts_to_add = [
        salary_discounts["INSS"],
        salary_discounts["Vale Transporte"],
    ]

    for discount in jovem_aprendiz_discounts_to_add:
        if discount not in existing_jovem_aprendiz_discounts:
            jovem_aprendiz_contract.discounts.add(discount)
            jovem_aprendiz_contract.log(
                USER,
                f"Associou o desconto '{discount.name}' ao contrato Jovem Aprendiz",
            )
            print(f"Desconto '{discount.name}' associado ao contrato Jovem Aprendiz.")

    # Verifica se os métodos de pagamento já foram configurados
    if not PaymentMethod.objects.exists():
        payment_methods = [
            {"name": "Mensal"},
            {"name": "Quinzenal"},
        ]

        for method in payment_methods:
            payment_method, created = PaymentMethod.objects.get_or_create(
                name=method["name"]
            )
            if created:
                payment_method.log(
                    USER,
                    f"Criou o método de pagamento '{method['name']}'",
                )
                print(f"Método de pagamento '{method['name']}' criado com sucesso.")

    # Verifica se as permissões já foram configuradas
    if not Permission.objects.exists():
        permissions_structure = {
            "E-commerce": {
                "Pedidos": ["Ver", "Editar", "Criar"],
                "Cupons": ["Ver", "Editar", "Criar"],
                "Layout": ["Ver", "Editar"],
                "Relatórios": ["Ver"],
                "Configuração": ["Ver", "Editar"],
            },
            "Funcionários": {
                "listagem": ["Ver", "Criar"],
                "perfil": {
                    "Ações": ["Ver", "Editar"],
                    "logs": ["Ver", "Editar"],
                },
                "Cargos": ["Ver", "Editar", "Criar"],
                "Permissões": ["Ver"],
            },
        }

        for parent_name, subcategories in permissions_structure.items():
            parent_permission, created = Permission.objects.get_or_create(
                name=parent_name
            )
            if created:
                parent_permission.log(
                    USER, f"Criou a permissão principal '{parent_name}'"
                )
                print(f"Criou a permissão principal '{parent_name}'")

            for category_name, actions in subcategories.items():
                category_permission, created = Permission.objects.get_or_create(
                    name=category_name, parent=parent_permission
                )
                if created:
                    category_permission.log(
                        USER,
                        f"Criou a permissão de categoria '{category_name}' sob '{parent_name}'",
                    )
                    print(
                        f"Criou a permissão de categoria '{category_name}' sob '{parent_name}'"
                    )

                for action in actions:
                    action_permission, created = Permission.objects.get_or_create(
                        name=action, parent=category_permission
                    )
                    if created:
                        action_permission.log(
                            USER,
                            f"Criou a permissão '{action}' sob '{category_name}'",
                        )
                        print(f"Criou a permissão '{action}' sob '{category_name}'")

    # Verifica se o cargo "Diretor" já foi configurado
    if not Role.objects.filter(name="Diretor").exists():
        director_role, created = Role.objects.get_or_create(name="Diretor", code="DR")
        if created:
            director_role.permissions.set(Permission.objects.all())
            director_role.log(USER, "Criou o cargo 'Diretor' com todas as permissões")
            print(f"Criou o cargo 'Diretor' com todas as permissões")

    # Verifica se o funcionário admin já foi configurado
    if not Employee.objects.filter(user=USER).exists():
        director_role = Role.objects.get(name="Diretor")
        clt_contract = ContractType.objects.get(name="CLT")
        admin_employee = Employee.objects.create(
            user=USER,
            full_name=USER.username,
            email=USER.email,
            cpf="000.000.000-00",
            birth_date="1990-01-01",
            rg="00000000-0",
            phone="(00) 00000-0000",
            start_time="09:00:00",
            end_time="18:00:00",
            gender="M",
            employment_status="active",
            contractType=clt_contract,
            role=director_role,
        )
        admin_employee.permissions.set(Permission.objects.all())
        admin_employee.log(
            USER,
            "Criou o funcionário admin com o cargo 'Diretor' com todas as permissões",
        )
        print(
            f"Criou o funcionário admin com o cargo 'Diretor' com todas as permissões"
        )


post_migrate.connect(setup_employee)
