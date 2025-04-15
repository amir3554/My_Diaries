from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext as trans


class Mood(models.IntegerChoices):
    SUPERHAPPY = 1, trans('SuperHappy')
    HAPPY = 2, trans('Happy')
    SATISFIED = 3, trans('Satisfied')
    FUNNY = 4, trans('Funny')
    LOVING = 5 , trans('Loving')
    NORMAL = 6, trans('Normal')
    NERVOUS = 7, trans('Nervous')
    SAD = 8, trans('Sad')
    UNSATISFIED = 9, trans('Unsatisfied')
    CRYING = 10, trans('Crying')
    ANGRY = 11, trans('Angry')

class Diary(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    mood = models.IntegerField(choices=Mood.choices, default=Mood.NORMAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    

class Notes(models.Model):
    description = models.CharField(max_length=255)
    important = models.BooleanField(default=False)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.description