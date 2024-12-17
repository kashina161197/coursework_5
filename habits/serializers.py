from rest_framework.serializers import ModelSerializer


from habits.models import Habit
from habits.validators import RelatedHabitOrRewordValidator, CheckLeadTimeValidator, RelatedHabitNotPleasantValidator, \
    IsPleasantNotRelatedHabitOrRewordValidator, DoingHabitLeastOnceWeek


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [RelatedHabitOrRewordValidator(field_1="related_habit", field_2="reward"),
                      CheckLeadTimeValidator(field="time_to_complete"),
                      RelatedHabitNotPleasantValidator(field="related_habit"),
                      IsPleasantNotRelatedHabitOrRewordValidator(field_1="sign_pleasant_habit", field_2="related_habit", field_3="reward"),
                      DoingHabitLeastOnceWeek(field="periodicity")]
