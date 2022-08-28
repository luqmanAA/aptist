from django import forms
from django.forms import formset_factory, modelformset_factory

from .models import Choice, Question


class CreateQuestionForm(forms.ModelForm):
    # choice_one = forms.CharField()
    # choice_two = forms.CharField()
    # QUESTION_CHOICES = [
    #     (choice_one, choice_one),
    #     (choice_two, choice_two)
    # ]
    # question = forms.CharField(max_length=250)
    # description = forms.CharField(max_length=250)
    # choice1 = forms.CharField(max_length=250)
    # choice2 = forms.CharField(max_length=250)
    # choice3 = forms.CharField(max_length=250)

    class Meta:
        model = Question
        fields = ['question_title', 'description']


class AddChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct']

    # def __int__(self, *args, **kwargs):
    #     super(AddChoiceForm, self).__int__(*args, **kwargs)
    #     data = kwargs.get('data')
    #     self.question_form = CreateQuestionForm(
    #         instance=self.instance and self.instance.choices,
    #         prefix=self.prefix, data=data
    #     )
    #
    # def clean(self):
    #     if not self.question_form.is_valid():
    #         raise forms.ValidationError("Choice not valid")
    #
    # def save(self, commit=True):
    #     question = super(AddChoiceForm, self).save(commit=commit)
    #     question.choices = self.question_form.save()
    #     question.save()


class QuestionForm(forms.ModelForm):
    question_title = forms.CharField(
        label='Question',
        widget=forms.Textarea(
            attrs={
                'cols': 20,
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'For example: If you were an animal, what would you be?'
            }
        ))
    description = forms.CharField(
        label='Details',
        widget=forms.Textarea(
            attrs={
                'cols': 20,
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'More information about the question (optional)'
            }
        ))

    class Meta:
        model = Question
        fields = ('question_title', 'description',)


class ChoiceForm(forms.ModelForm):
    choice_text = forms.CharField(
        label='Choice',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your answer option'
        })
    )

    class Meta:
        model = Choice
        fields = ('choice_text', 'is_correct',)


ChoiceFormset = formset_factory(ChoiceForm, extra=3)

# class ChoiceForm(forms.ModelForm):





# ChoiceFormset = modelformset_factory(
#     Choice,
#     fields=('choice_text',),
#     extra=2,
#     labels={'choice_text': 'Choice'},
#     widgets={
#         'choice_text': forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter your answer option'
#             }
#         )
#     }
# )