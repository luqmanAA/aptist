from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse

from applicants.models import Applicant

from .forms import SignUpForm
from .models import Organization

# Create your views here.

# Organization register view


class CreateOrganizationView(FormView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password2')
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return ('/')


class OrganizationDetailView(DetailView):
    model = Organization


class UpdateOrganizationView(UpdateView):
    model = Organization
    template_name_suffix = '_update'
    fields = (
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'company_name',
        'company_size',
    )

    def get_success_url(self):
        return reverse(
            'accounts:organization',
            kwargs={'slug': self.kwargs['slug'],}
        )




