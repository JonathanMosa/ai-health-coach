from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Creates a User and its linked UserProfile in a single request."""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    experience_level = serializers.ChoiceField(
        choices=UserProfile.ExperienceLevel.choices
    )
    fitness_goal = serializers.ChoiceField(choices=UserProfile.FitnessGoal.choices)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "experience_level",
            "fitness_goal",
        ]

    def create(self, validated_data):
        experience_level = validated_data.pop("experience_level")
        fitness_goal = validated_data.pop("fitness_goal")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        UserProfile.objects.create(
            user=user,
            experience_level=experience_level,
            fitness_goal=fitness_goal,
        )
        return user
