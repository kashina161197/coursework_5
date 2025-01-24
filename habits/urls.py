from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitListAPIView, HabitViewSet

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"habit", HabitViewSet, basename="habit")

urlpatterns = [
    path("habit_list_public/", HabitListAPIView.as_view(), name="habit_list_public"),
] + router.urls
