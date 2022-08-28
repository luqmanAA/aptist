from django.db import models

from applicants.models import Applicant
from assessments.models import Assessment


# Create your models here.


class Result(models.Model):
    assessments = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='results',
    )
    applicants = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        related_name='results',
    )
    score = models.FloatField()

    def __str__(self):
        return f"{self.score}, applicant: {self.applicants}, assessment: {self.assessments.name}"
