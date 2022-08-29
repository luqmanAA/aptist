from ast import arg
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
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
    company_name=''

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                organization = Organization.objects.get(id=request.user.id)
                return HttpResponseRedirect(
                    reverse('accounts:organization', args=[organization.slug])
                )
            except:
                return HttpResponse('/')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        self.company_name = form.cleaned_data.get('company_name').lower()
        self.company_name = self.company_name.replace(' ', '-')
        password = form.cleaned_data.get('password2')
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return (reverse('accounts:organization', args=[self.company_name]))


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization


class UpdateOrganizationView(LoginRequiredMixin, UpdateView):
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


def redirect_profile_view(request):
    organization = Organization.objects.filter(id=request.user.id).first()
    return HttpResponseRedirect(
        reverse('assessments:home')
    )
    
    
class DashboardView(View):
    pass