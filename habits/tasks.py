from celery import shared_task
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def check_habits():
    """Задача отправки уведомления на выполнение привычки"""

    habits = Habit.objects.filter(owner__tg_chat_id__isnull=False)

    for habit in habits:
        print(habit)
        tg_chat_id = habit.owner.tg_chat_id

        if habit.place:
            message = f"Пришло время {habit.action} в {habit.place}"
        else:
            message = f"Пришло время {habit.action}"
        send_telegram_message(tg_chat_id, message)
        habit.time += habit.get_periodicity_timedelta()
        print(habit.time)
        habit.save()
