import uuid

from django.db import models

from accounts.models import Organization
from applicants.models import Applicant

# Create your models here.


class ActiveObject(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True, is_deleted=False
            )


class DeletedObject(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField(
        help_text='Time(in HH:MM:SS format.) to be allocated to assessment'
    )
    pass_mark = models.IntegerField(help_text='Pass mark in percentage')
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='assessments'
    )
    
    active_objects = ActiveObject()
    deleted_objects = DeletedObject()
    objects = models.Manager()

    class Meta:
        permissions = (("can_view_all", "View all pages"),)

    def __str__(self):
        return self.name
    
   


# class AssessmentTaken(models.Model):
#     assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
#     applicant = models.ForeignKey(
#         Applicant,
#         on_delete=models.CASCADE,
#         related_name='assessment_taken'
#     )
#     started_at = models.DateTimeField(auto_now_add=True)
#     question_answered = models.ManyToManyField(
#         'questions.QuestionAnswered',
#         related_name='assessment_taken',
#     )
#     selected_choice = models.ManyToManyField(
#         'questions.SelectedChoice',
#         related_name='assessment_taken',
#     )
#     duration_left = models.DurationField()
#     is_completed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"AssessmentTaken: {self.assessment.name}"


# class AssessmentStarted(models.Model):
#     started_at = models.DateTimeField(auto_now_add=True)
#     assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
#     applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"AssessmentStarted: {self.assessment.name} by {self.applicant}"