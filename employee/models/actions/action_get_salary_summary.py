from .action_calculate_adjustments import action_calculate_adjustments
def action_get_salary_summary(employee, start_date=None, end_date=None):
    """
    Retorna um resumo completo do salário, incluindo bruto, líquido, descontos e ajustes.
    """
    net_salary = employee.calculate_net_salary()
    discounts = employee.get_salary_discounts()
    adjustments = action_calculate_adjustments(employee, start_date, end_date)

    return {
        "gross_salary": (
            employee.salaries.order_by("-start_date").first().gross_salary
            if employee.salaries.exists()
            else 0
        ),
        "net_salary": net_salary,
        "discounts": discounts,
        "adjustments": adjustments,
    }
