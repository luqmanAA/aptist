from pytimeparse.timeparse import timeparse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import Assessment
from accounts.models import Organization


# Create your views here.


class CreateAssessmentView(LoginRequiredMixin, CreateView):
    model = Assessment
    template_name_suffix = '_create'
    fields = (
        'name',
        'duration',
        'pass_mark'
    )

    def form_valid(self, form):
        organization = Organization.objects.filter(
            email=self.request.user.email
        ).first()
        form.instance.created_by = organization
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('assessments:detail', args=[self.object.id])


class EditAssessmentView(LoginRequiredMixin, UpdateView):
    model = Assessment
    template_name_suffix = '_update'
    fields = (
        'name',
        'duration',
        'pass_mark',
        'is_published',
    )

    def get_success_url(self):
        return reverse('assessments:detail', args=[self.object.id])


class AssessmentListView(LoginRequiredMixin, ListView):
    model = Assessment


class AssessmentDetailView(LoginRequiredMixin, DetailView):
    model = Assessment
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessment = self.get_object()
        context['duration_in_time'] = assessment.duration.total_seconds()/60
        return context
        


class ToggleAssessmentVisibilityView(LoginRequiredMixin, View):

    def get(self, request, pk, **kwargs):
        assessment = Assessment.objects.filter(id=pk).first()
        assessment.is_published = not assessment.is_published
        assessment.save()
        return HttpResponseRedirect(reverse('assessments:home'))
