from django.db import models
import datetime
from users.models import CustomsUser


class Habit(models.Model):
    """Модель привычки"""

    OWNER_CHOICES = [
        ("every hour", "каждый час"),
        ("every day", "каждый день"),
        ("every other day", "через день"),
        ("every three days", "раз в 3 дня"),
        ("every four days", "раз в 4 дня"),
        ("every five days", "раз в 5 дней"),
        ("every six days", "раз в 6 дней"),
        ("every week", "раз в неделю"),
    ]

    owner = models.ForeignKey(
        CustomsUser,
        verbose_name="Владелец",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    place = models.CharField(max_length=150, blank=True, null=True, verbose_name="Место выполнения привычки", help_text="Укажите место, в котором необходимо выполнять привычку")
    time = models.DateTimeField(null=True, blank=True, verbose_name="Время выполнения привычки", help_text="Укажите время, когда необходимо выполнять привычку")
    action = models.CharField(max_length=150, verbose_name="Действие привычки", help_text="Укажите действие, которое представляет собой привычка")
    sign_pleasant_habit = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Привычка является приятной",
    )

    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Выберете связанную приятную привычку",
    )
    periodicity = models.CharField(
        max_length=16,
        choices=OWNER_CHOICES,
        verbose_name="Периодичность выполнения",
        help_text="Выберите периодичность выполнения привычки",
        default="every day",
    )
    reward = models.CharField(
        max_length=255,
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение",
        blank=True,
        null=True,
    )
    time_to_complete = models.IntegerField(
        default=1,
        verbose_name="Время выполнения",
        help_text="Укажите предположительное время выполнения привычки в минутах",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Общий доступ",
        help_text="Опубликовать привычку для общего доступа",
    )

    def __str__(self):
        return f"{self.action} by {self.owner.username} at {self.place}"

    def get_periodicity_timedelta(self):
        if self.periodicity == "every hour":
            return datetime.timedelta(hours=1)
        elif self.periodicity == "every day":
            return datetime.timedelta(days=1)
        elif self.periodicity == "every other day":
            return datetime.timedelta(days=2)
        elif self.periodicity == "every three days":
            return datetime.timedelta(days=3)
        elif self.periodicity == "every four days":
            return datetime.timedelta(days=4)
        elif self.periodicity == "every five days":
            return datetime.timedelta(days=5)
        elif self.periodicity == "every six days":
            return datetime.timedelta(days=6)
        elif self.periodicity == "every week":
            return datetime.timedelta(weeks=1)
        else:
            return None

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["action"]
