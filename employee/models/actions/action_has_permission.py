def action_has_permission(employee, permission_name):
    """
    Verifica se o funcionário possui uma permissão específica.
    """
    # Verifica se a permissão está vinculada diretamente ao funcionário
    if employee.permissions.filter(name=permission_name).exists():
        return True

    # Verifica se a permissão está vinculada ao cargo do funcionário
    if (
        employee.role
        and employee.role.permissions.filter(name=permission_name).exists()
    ):
        return True

    return False
