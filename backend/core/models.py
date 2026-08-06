from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserProfile(models.Model):
    class ExperienceLevel(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    class FitnessGoal(models.TextChoices):
        MUSCLE_GAIN = "muscle_gain", "Muscle Gain"
        WEIGHT_LOSS = "weight_loss", "Weight Loss"
        GENERAL_FITNESS = "general_fitness", "General Fitness"
        STRENGTH = "strength", "Strength"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    experience_level = models.CharField(
        max_length=20, choices=ExperienceLevel.choices
    )
    fitness_goal = models.CharField(max_length=20, choices=FitnessGoal.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class WorkoutPlan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workout_plans",
    )
    week_start_date = models.DateField()
    plan_data = models.JSONField(
        help_text="Structured weekly plan as returned by the LLM."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "week_start_date")
        ordering = ["-week_start_date"]

    def __str__(self):
        return f"{self.user.username} - week of {self.week_start_date}"


class WorkoutLog(models.Model):
    class MuscleGroup(models.TextChoices):
        CHEST = "chest", "Chest"
        BACK = "back", "Back"
        LEGS = "legs", "Legs"
        SHOULDERS = "shoulders", "Shoulders"
        ARMS = "arms", "Arms"
        CORE = "core", "Core"
        FULL_BODY = "full_body", "Full Body"

    plan = models.ForeignKey(
        WorkoutPlan, on_delete=models.CASCADE, related_name="logs"
    )
    date = models.DateField()
    exercise_name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=20, choices=MuscleGroup.choices)
    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.exercise_name} on {self.date}"


class CheckIn(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="check_ins"
    )
    date = models.DateField()
    sleep_hours = models.DecimalField(max_digits=3, decimal_places=1)
    soreness_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    energy_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} check-in - {self.date}"
