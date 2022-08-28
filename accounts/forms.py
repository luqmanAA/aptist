from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Organization


class SignUpForm(UserCreationForm):

    class Meta:
        model = Organization
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'company_name',
            'company_size',
        )
