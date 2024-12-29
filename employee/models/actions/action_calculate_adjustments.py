def action_calculate_adjustments(employee, start_date=None, end_date=None):
    """
    Calcula os ajustes (adições e subtrações) baseados em um intervalo de datas.
    """
    total_add = 0
    total_subtract = 0
    detailed_adjustments = []

    filters = {}
    if start_date:
        filters["created_at__date__gte"] = start_date
    if end_date:
        filters["created_at__date__lte"] = end_date

    # Executar a consulta no banco de dados com os filtros
    adjustments = employee.adjustments.filter(**filters)

    # Processar os ajustes
    for adjustment in adjustments:
        if adjustment.adjustment_type == "add":
            total_add += adjustment.amount
            value = f"+{adjustment.amount}"
        elif adjustment.adjustment_type == "subtract":
            total_subtract += adjustment.amount
            value = f"-{adjustment.amount}"

        detailed_adjustments.append(
            {
                "description": adjustment.description,
                "value": value,
                "applied_date": adjustment.created_at.date(),
            }
        )

    return {
        "total_add": total_add,
        "total_subtract": total_subtract,
        "detailed_adjustments": detailed_adjustments,
    }
