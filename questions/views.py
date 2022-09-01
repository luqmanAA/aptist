import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, FormView

from accounts.models import Organization
from assessments.models import Assessment

from .forms import CreateQuestionForm, AddChoiceForm, QuestionForm, ChoiceFormset
from .models import Question, Choice


# Create your views here.

@login_required
def create_question_with_choices(request, assessment_id):
    assessment = Assessment.objects.filter(id=assessment_id).first()
    
    # check if the request to this view is POST then bound it to the forms
    if request.method == 'POST':
        formdata = request.POST.dict()
        question_title = formdata.pop('question_title')
        if 'description' in formdata:
            description = formdata.pop('description')
        else:
            description = None
        choices = formdata      

        question = Question.objects.create(
            assessments_id = assessment_id,
            question_title=question_title,
            description=description,
            )
        # loop through the set of choice to create choice object for each
        for choice in choices:
            if choices[choice] == 'true':
                Choice.objects.create(
                    choice_text=choice, is_correct=True, question=question)
            else:
                Choice.objects.create(
                    choice_text=choice, question=question)

        redirect_url = reverse('assessments:detail', args=[assessment_id])
        return JsonResponse(
            {'redirect_url': redirect_url}
        )
    else:
        # return empty forms if request is not POST
        question_form = QuestionForm()
        # choice_formset = ChoiceFormset()
    return render(
        request,
        'questions/question_create.html',
        {
            'assessment': assessment,
            'question_form': question_form,
            'organization': assessment.created_by
            # 'choice_formset': choice_formset,
        })


# class CreateQuestionView(FormView):
#     form_class = AddChoiceForm
#     template_name = 'questions/question_create.html'


class EditQuestionView(UpdateView):
    model = Question
    template_name_suffix = '_update'
    fields = (
        'question_title',
        'description',
        'assessments',
    )

    def get_success_url(self):
        return reverse('assessments:questions:detail', args=[self.object.id])


class QuestionListView(ListView):
    model = Question
    paginate_by = 5
    
    def get_queryset(self):
        assessment_id = self.kwargs['assessment_id']
        return Question.objects.filter(assessments_id=assessment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = Organization.objects.get(id=self.request.user.id)
        context['question'] = self.object_list.first()
        context['assessment_id'] = self.kwargs['assessment_id']
        context['organization'] = organization
        return context


class QuestionDetailView(DetailView):
    model = Question

