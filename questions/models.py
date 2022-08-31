from django.db import models

from assessments.models import Assessment

# Create your models here.


class Question(models.Model):
    question_title = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True, blank=True)
    assessments = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='questions',
        related_query_name='question'
    )

    def __str__(self):
        return self.question_title

    def get_question_choices(self):
        return self.choices


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        related_query_name='choice',
    )

    def __str__(self):
        return f"{self.choice_text} " \
               f"for question: {self.question.question_title}"

    def get_selected_choice(self):
        return self.selected_choice


# class QuestionAnswered(models.Model):
#     question = models.ForeignKey(
#         Question,
#         on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return self.question.question_title

#     def get_selected_choice(self):
#         return self.selected_choice.choice.choice_text


# class SelectedChoice(models.Model):
#     question_answered = models.OneToOneField(
#         QuestionAnswered,
#         on_delete=models.CASCADE,
#         related_name='selected_choice'
#     )
#     choice = models.OneToOneField(
#         Choice,
#         on_delete=models.CASCADE,
#         related_name='selected_choice',
#         null=True,
#         blank=True
#     )
#     none_choice = models.CharField(max_length=200, null=True, blank=True)

#     def __str__(self):
#         return f"{self.choice.choice_text} " \
#                f"for question: {self.choice.question.question_title}"
