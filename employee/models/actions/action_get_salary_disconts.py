def action_get_salary_disconts(self):
    discounts = []
    salary = self.salaries.order_by("-start_date").first()
    if not salary or not self.contractType:
        return discounts

    for discount in self.contractType.discounts.all():
        for bracket in discount.brackets.all():
            if salary.gross_salary > bracket.min_value and (
                not bracket.max_value or salary.gross_salary <= bracket.max_value
            ):
                discount_amount = salary.gross_salary * bracket.percentage / 100
                discounts.append(
                    {
                        "name": discount.name,
                        "amount": discount_amount,
                        "percentage": bracket.percentage,
                        "range": f"{bracket.min_value} - {bracket.max_value or 'Acima'}",
                    }
                )
                break
    return discounts
