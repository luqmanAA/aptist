from datetime import datetime, timedelta
import json
from pytimeparse.timeparse import timeparse

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView, FormView

from accounts.models import User
from assessments.models import Assessment
from questions.models import Choice
from results.models import Result

from .models import Applicant

# Create your views here.


class CreateApplicantView(CreateView):
    model = Applicant
    fields = ('first_name', 'last_name', 'email')
    template_name = 'applicants/register.html'

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
        
        return (self.request.META.get('HTTP_REFERER'))            


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
                'applicants:test-tip',
                args=[pk]
            )
        )


class StartAssessmentView(View):
    db_objects = {}

    def get(self, request, pk, **kwargs):
        try:
            assessment = Assessment.active_objects.get(id=pk)
            applicant = Applicant.objects.get(account_id=request.user.id)
            self.db_objects.update({
                'assessment': assessment,
                'applicant': applicant,
            })
            
            if not Result.objects.filter(
                    assessment=assessment,
                    applicant=applicant
                    ).exists():
                result = Result.objects.create(
                    assessment=assessment,
                    applicant=applicant,
                    )
            else:
                result = Result.objects.filter(
                    assessment=assessment
                    ).first()
            self.db_objects.update({
                'result': result
            })
            time_to_complete = result.time_started + assessment.duration
            time_now = datetime.now()
            if time_now > time_to_complete:
                context = {
                    'prompt_title': "Time is over!",
                    'prompt_body': "You've exhausted the time allocated for the assessment"
                }
                return render(
                    request,
                    'prompt.html',
                    context=context
                )
            print("from get",self.db_objects)
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
            if request.user.is_authenticated:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Only applicants can take the assessment")
                return HttpResponseRedirect(
                    reverse('accounts:profile')
                )
            return render(
                request,
                'applicants/register.html'
            )
        except Assessment.DoesNotExist:
            context = {
                'prompt_title': "No such assessment exist",
                'prompt_body': "Sorry, couldn't find the assessment you're trying to take.\
                    Contact admin to get the right link"
            }
            return render(
                request,
                'prompt.html',
                context=context
            )

    def post(self, request, pk):
        print('from post',self.db_objects)
        assessment = self.db_objects['assessment']
        print(assessment)
        # applicant = self.db_objects.get('applicant')
        result = self.db_objects.get('result')
        correct_choice_list = []
        print(assessment)
        question_records = assessment.questions.all()
        
        for question in question_records:
            correct_choice = question.choices.filter(is_correct=True).first()
            if correct_choice:
                correct_choice_list.append(correct_choice.choice_text)
        assessment_data = (request.POST).dict()
        time_completed_in_seconds = timeparse(
            assessment_data.pop('time_completed', '')
            )
        if time_completed_in_seconds:
            time_completed_in_delta = timedelta(
                seconds=time_completed_in_seconds
            )
            result.time_taken = assessment.duration - time_completed_in_delta
            
        selected_answer_list = list(assessment_data.values())
        all_questions = list(assessment_data.keys())
        attempted_questions = list({
            question for question in assessment_data
            if assessment_data[question] != 'null'
            })
        correct_answers = [i for i in selected_answer_list if i in correct_choice_list]

        score = (len(correct_answers) / len(correct_choice_list))
        print(len(all_questions))
        print(len(attempted_questions))
        print(len(correct_choice_list))
        print(len(correct_answers))
        print(result)
        
        result.number_of_attempted_questions = len(attempted_questions)
        result.number_of_correct_answers = len(correct_answers)
        result.number_of_incorrect_answers = len(
            correct_choice_list) - len(correct_answers)
        result.percentage_score = score * 100
        result.save()

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

