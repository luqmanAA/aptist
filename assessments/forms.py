from django.forms import ModelForm

from .models import Assessment


class CreateAssessmentForm(ModelForm):
    
    class Meta:
        model = Assessment
        fields = (
            'name',
            'description',
            'duration',
            'pass_mark',
            )