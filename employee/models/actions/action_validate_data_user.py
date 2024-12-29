from accounts.models.user import User


def action_validate_data_user(cls, data):
    """
    Valida os dados de documentos e login antes de criar o usuário.
    """
    # Verifica CPF
    existing_cpf = cls.objects.filter(cpf=data["cpf"]).first()
    if existing_cpf:
        raise ValueError(
            f"O CPF {data['cpf']} já está cadastrado para o funcionário {existing_cpf.full_name}."
        )

    # Verifica RG
    existing_rg = cls.objects.filter(rg=data["rg"]).first()
    if existing_rg:
        raise ValueError(
            f"O RG {data['rg']} já está cadastrado para o funcionário {existing_rg.full_name}."
        )

    # Verifica CNH
    if data.get("cnh"):
        existing_cnh = cls.objects.filter(cnh=data["cnh"]).first()
        if existing_cnh:
            raise ValueError(
                f"A CNH {data['cnh']} já está cadastrada para o funcionário {existing_cnh.full_name}."
            )

    # Verifica se o email do usuário já está cadastrado
    if User.objects.filter(email=data["user_email"]).exists():
        raise ValueError(
            f"O e-mail de acesso {data['user_email']} já está em uso por outro usuário."
        )
