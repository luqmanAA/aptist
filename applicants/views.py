from datetime import datetime, timedelta
import json
from pytimeparse.timeparse import timeparse

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView, FormView

from accounts.models import User
from assessments.models import Assessment, AssessmentTaken
from questions.models import Choice, QuestionAnswered, SelectedChoice

from .models import Applicant

# Create your views here.


class CreateApplicantView(CreateView):
    model = Applicant
    fields = ('first_name', 'last_name', 'email')
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form, **kwargs):
        applicant = form.save(commit=False)
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.create(email=email)
            applicant.account_id = user.id
            applicant.save()
            login(self.request, user)
            return super().form_valid(form)
        except IntegrityError:
            messages.add_message(
                self.request,
                messages.ERROR,
                "An applicant with the same email already exists!"
            )
            return super().get(self.request, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return ('/')


class AssessmentTipView(View):

    def get(self, request, pk, **kwargs):
        assessment = get_object_or_404(Assessment, id=pk)
        number_of_question = assessment.questions.count()
        duration = assessment.duration
        organization_name = assessment.created_by.company_name
        applicant_name = request.user.first_name
        context = {
            'applicant_name': applicant_name,
            'number_of_question': number_of_question,
            'duration': duration,
            'organization_name': organization_name
        }
        return render(
            request,
            'applicants/test_tip.html',
            context=context
        )

    def post(self, request, pk, **kwargs):
        return HttpResponseRedirect(
            reverse(
                'applicants:start-test',
                args=[pk]
            )
        )


class StartAssessmentView(View):
    db_objects = {}

    def get(self, request, pk, **kwargs):
        try:
            assessment = Assessment.objects.get(id=pk)
            applicant = Applicant.objects.get(account_id=request.user.id)
            self.db_objects.update({
                'assessment': assessment,
                'applicant': applicant,
            })
            if not AssessmentTaken.objects.filter(
                    assessment=assessment,
                    applicant=applicant
                    ).exists():
                assessment_taken = AssessmentTaken.objects.create(
                    assessment=assessment,
                    applicant=applicant,
                    duration_left=assessment.duration)
            else:
                assessment_taken = AssessmentTaken.objects.filter(
                    assessment=assessment
                    ).first()
            self.db_objects.update({
                'assessment_taken': assessment_taken
            })
            time_to_complete = assessment_taken.started_at + assessment.duration
            time_now = datetime.now()
            if time_now > time_to_complete:
                return HttpResponseRedirect('/')

            context = {
                'time_to_complete': time_to_complete,
                'assessment': assessment,
            }
            return render(
                request,
                'applicants/take_test.html',
                context=context
            )

        except Applicant.DoesNotExist:
            messages.add_message(
                request,
                messages.ERROR,
                "Only applicants can take the assessment")
            return HttpResponseRedirect('/')

        except Assessment.DoesNotExist:
            messages.add_message(
                request,
                messages.ERROR,
                "Sorry, you got the wrong url, the assessment you're trying to view does not exist")
            return HttpResponseRedirect('/')

    def post(self, request, pk):
        assessment_taken = self.db_objects.get('assessment_taken', '')
        request_data = (request.POST).dict()
        time_completed_in_string = request_data.pop('time_completed','')
        time_completed_in_seconds = timeparse(time_completed_in_string)
        if time_completed_in_seconds:
            time_completed_in_delta = timedelta(
                seconds=time_completed_in_seconds
            )
            assessment_taken.duration_left = time_completed_in_delta
        assessment_result = request_data

        for question in assessment_result:
            if assessment_result[question] == 'null':
                selected_choice_text = 'not answered'
            else:
                selected_choice_text = assessment_result[question]
            if QuestionAnswered.objects.filter(question_id=question).exists():
                question_answered = QuestionAnswered.objects.filter(question_id=question).first()
            else:
                question_answered = QuestionAnswered.objects.create(
                    question_id=question
                )
            if Choice.objects.filter(
                    choice_text__iexact=selected_choice_text,
                    question_id=question
                    ).exists():
                choice = Choice.objects.filter(
                    choice_text__iexact=selected_choice_text,
                    question_id=question).first()
                selected_choice = SelectedChoice(
                    question_answered=question_answered,
                    choice=choice
                )
            else:
                selected_choice = SelectedChoice(
                    question_answered=question_answered,
                    none_choice=selected_choice_text
                )
            selected_choice.save()
            assessment_taken.question_answered.add(question_answered)
            assessment_taken.selected_choice.add(selected_choice)
            assessment_taken.save()

        redirect_url = reverse('applicants:assessment-completed', args=[pk])
        return JsonResponse(
            {'redirect_url': redirect_url}
        )

#
# def take_test_view(request, pk):
#     assessment = get_object_or_404(Assessment, id=pk)
#
#     if request.method == 'POST':
#         assessment_result = request.POST
#         applicant = get_object_or_404(Applicant, account_id=request.user.id)
#         assessment_taken = AssessmentTaken(assessment_id=assessment.id)
#
#         for question in assessment_result:
#             if assessment_result[question] == 'null':
#                 selected_choice = 'not answered'
#             else:
#                 selected_choice = assessment_result[question]
#             assessment_taken.question = question
#             assessment_taken.selected_choice = selected_choice
#             assessment_taken.applicant = applicant
#             assessment_taken.save()
#
#         return JsonResponse(reverse(
#             ''
#         ))
#
#     context = {
#         'assessment': assessment,
#     }
#     return render(
#         request,
#         'applicants/take_test.html',
#         context=context
#     )


class AssessmentCompleteView(View):

    def get(self, request, **kwargs):
        return HttpResponse("Well done, you've completed assessment")

