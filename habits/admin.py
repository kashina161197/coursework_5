from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "time",
        "action",
    )
    search_fields = ("owner",)
