from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import CustomsUser


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = CustomsUser.objects.create(email="test@gmail.com")
        self.habit = Habit.objects.create(
            owner=self.user,
            time="2024-12-05 07:00",
            action="Test",
            periodicity="every day",
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Тестирование создания привычки"""

        data = {
            "time": "2024-12-06 10:00",
            "action": "Test",
            "periodicity": "every day",
        }
        response = self.client.post(
            "/habit/",
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_create_with_unpleasant_related_habit(self):
        """Тестирование отношение связанной привычки к приятной"""

        related_habit = Habit.objects.create(
            owner=self.user,
            time="2024-12-05 07:00",
            action="Unpleasant Habit",
            periodicity="every day",
            time_to_complete=1,
            sign_pleasant_habit=False,
        )
        data = {
            "time": "2024-12-06 10:00",
            "action": "Test",
            "periodicity": "every day",
            "time_to_complete": 1,
            "related_habit": related_habit.pk,
        }
        response = self.client.post("/habit/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Связанная привычка должна быть приятной", str(response.json()))

    def test_habit_create_with_related_habit_and_reward(self):
        """Тестирование не использовать одновременно связанную привычку и вознаграждение"""

        related_habit = Habit.objects.create(
            owner=self.user,
            time="2024-12-05 07:00",
            action="related_habit",
            periodicity="every day",
            time_to_complete=1,
            sign_pleasant_habit=True,
        )

        data = {
            "time": "2024-12-06 10:00",
            "action": "Test",
            "periodicity": "every day",
            "time_to_complete": 1,
            "related_habit": related_habit.pk,
            "reward": "chocolate",
        }
        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя использовать одновременно связанную привычку и вознаграждение",
            str(response.json()),
        )

    def test_habit_create_with_wrong_lead_time(self):
        """Тестирование время выполнения привычки"""

        data = {
            "time": "2024-12-06 10:00",
            "action": "Test",
            "periodicity": "every day",
            "time_to_complete": 121,
        }
        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Время выполнения должно быть не больше 120 минут", str(response.json())
        )

    def test_habit_is_pleasant_create_with_reward(self):
        """Тестирование отсутствие у приятной привычки связанной привычки или вознаграждения"""

        data = {
            "time": "2024-12-06 10:00",
            "action": "Test",
            "periodicity": "every day",
            "time_to_complete": 1,
            "is_pleasant": True,
            "reward": "chocolate",
        }
        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть связанной привычки или вознаграждения",
            str(response.json()),
        )

    def test_habit_retrieve(self):
        """Тестирование просмотра привычки"""

        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_update(self):
        """Тестирование редактирования привычки."""

        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {"action": "Test1"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Test1")

    def test_habit_delete(self):
        """Тестирование удаления привычки"""

        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
