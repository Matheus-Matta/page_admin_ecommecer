from datetime import datetime, timedelta


def format_last_login(date_string):
    now = datetime.now()  # Data atual
    target_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")  # Data fornecida
    difference = now - target_date  # Diferença em timedelta

    one_minute = timedelta(minutes=1)
    one_hour = timedelta(hours=1)
    one_day = timedelta(days=1)
    one_week = timedelta(weeks=1)
    one_month = timedelta(days=30)
    one_year = timedelta(days=365)

    if difference < one_hour:
        minutes = difference // one_minute
        return f"{minutes} minuto{'s' if minutes != 1 else ''} atrás"
    elif difference < one_day:
        hours = difference // one_hour
        return f"{hours} hora{'s' if hours != 1 else ''} atrás"
    elif difference < one_week:
        days = difference // one_day
        return f"{days} dia{'s' if days != 1 else ''} atrás"
    elif difference < one_month:
        weeks = difference // one_week
        return f"{weeks} semana{'s' if weeks != 1 else ''} atrás"
    elif difference < one_year:
        months = difference // one_month
        return f"{months} mês{'es' if months != 1 else ''} atrás"
    else:
        years = difference // one_year
        return f"{years} ano{'s' if years != 1 else ''} atrás"
