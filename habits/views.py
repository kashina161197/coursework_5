from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from courses.tasks import newsletter_about_updating_course_materials
from users.permissions import IsOwner

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD привычек."""
    queryset = Habit.objects.all()
    pagination_class = HabitPagination
    serializer_class = HabitSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class HabitListAPIView(generics.ListAPIView):
    """Список публичных привычек"""

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]
