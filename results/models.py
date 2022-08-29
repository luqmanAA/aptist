from django.db import models

from applicants.models import Applicant
from assessments.models import Assessment


# Create your models here.


class Result(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='results',
    )
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        related_name='results',
    )
    number_of_attempted_questions = models.IntegerField(null=True, blank=True)
    number_of_correct_answers = models.IntegerField(null=True, blank=True)
    number_of_incorrect_answers = models.IntegerField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    percentage_score = models.FloatField(null=True, blank=True)
    time_started = models.DateTimeField(auto_now_add=True, null=True)
    time_taken = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.score}"
    
    def get_number_of_applicants(self):
        return self.applicant.all()
