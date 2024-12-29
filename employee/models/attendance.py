from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.mixin import LoggableMixin
from .employee import Employee
from datetime import date


class Attendance(LoggableMixin, models.Model):
    # Relaciona o ponto ao funcionário
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="attendances"
    )

    # Data do ponto
    date = models.DateField(verbose_name=_("Data"))

    # Registro dos horários
    first_entry = models.TimeField(
        blank=True, null=True, verbose_name=_("Primeira Entrada")
    )
    first_exit = models.TimeField(
        blank=True, null=True, verbose_name=_("Primeira Saída")
    )
    second_entry = models.TimeField(
        blank=True, null=True, verbose_name=_("Segunda Entrada")
    )
    second_exit = models.TimeField(
        blank=True, null=True, verbose_name=_("Segunda Saída")
    )

    # Status do ponto
    status = models.CharField(
        max_length=20,
        choices=[
            ("complete", "Completo"),
            ("incomplete", "Incompleto"),
            ("absent", "Falta"),
        ],
        default="absent",
        verbose_name=_("Status"),
    )

    # Observações adicionais
    observation = models.TextField(blank=True, null=True, verbose_name=_("Observação"))

    class Meta:
        verbose_name = _("Ponto")
        verbose_name_plural = _("Pontos")
        ordering = ["-date"]

    def __str__(self):
        return f"Ponto de {self.employee.user.full_name} em {self.date}"

    def calculate_hours(self):
        """
        Calcula o total de horas trabalhadas no dia.
        """
        from datetime import datetime

        def time_difference(start, end):
            if start and end:
                return (
                    datetime.combine(date.min, end) - datetime.combine(date.min, start)
                ).seconds / 3600
            return 0

        return time_difference(self.first_entry, self.first_exit) + time_difference(
            self.second_entry, self.second_exit
        )

    def save(self, *args, **kwargs):
        """
        Atualiza automaticamente o status baseado nos registros de ponto.
        """
        entries = [
            self.first_entry,
            self.first_exit,
            self.second_entry,
            self.second_exit,
        ]
        filled_entries = [entry for entry in entries if entry]

        if len(filled_entries) == 4:
            self.status = "complete"
        elif len(filled_entries) > 0:
            self.status = "incomplete"
        else:
            self.status = "absent"

        super().save(*args, **kwargs)

    @staticmethod
    def calculate_overtime(employee, start_date, end_date):
        """
        Calcula o banco de horas para um funcionário entre duas datas.
        """
        from datetime import timedelta

        attendances = Attendance.objects.filter(
            employee=employee, date__range=(start_date, end_date)
        )

        total_hours = sum(attendance.calculate_hours() for attendance in attendances)
        standard_hours = len(attendances) * 8  # Considera 8 horas padrão por dia
        return total_hours - standard_hours
