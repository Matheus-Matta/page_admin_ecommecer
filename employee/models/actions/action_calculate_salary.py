def action_calculate_salary(self):
    # Obter o salário bruto mais recente
    salary = self.salaries.order_by("-start_date").first()
    if not salary:
        return 0  # Sem salário registrado

    # Calcular descontos associados ao tipo de contrato
    total_discounts = 0
    if self.contractType:
        for discount in self.contractType.discounts.all():
            for bracket in discount.brackets.all():
                if salary.gross_salary > bracket.min_value and (
                    not bracket.max_value or salary.gross_salary <= bracket.max_value
                ):
                    total_discounts += salary.gross_salary * bracket.percentage / 100
                    break

    # Calcular ajustes (adições e subtrações)
    total_adjustments = salary.calculate_adjustments()

    # Salário líquido = bruto - descontos + ajustes
    return salary.gross_salary - total_discounts + total_adjustments
