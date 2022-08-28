from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, FormView

from .forms import CreateQuestionForm, AddChoiceForm, QuestionForm, ChoiceFormset
from .models import Question, Choice


# Create your views here.


def create_question_with_choices(request, assessment_id):

    # check if the request to this view is POST then bound it to the forms
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormset(request.POST)

        # validate the forms
        if question_form.is_valid() and choice_formset.is_valid():

            # create question object form question form but don't save yet
            question = question_form.save(commit=False)

            # attach the assessment on which the question is created to it
            question.assessments_id = assessment_id

            # then save
            question.save()

            # loop through the set of choice form to create choice object for each
            for choice_form in choice_formset:
                choice_data = choice_form.cleaned_data.get('choice_text')
                is_correct = choice_form.cleaned_data.get('is_correct')
                if choice_data:
                    # create choice object but don't save yet
                    choice = Choice(choice_text=choice_data, is_correct=is_correct)

                    # attach the question the choice belongs to
                    choice.question = question

                    # now save
                    choice.save()

            return HttpResponseRedirect(
                reverse('assessments:detail', args=[assessment_id])
            )
    else:
        # return empty forms if request is not POST
        question_form = QuestionForm()
        choice_formset = ChoiceFormset()
    return render(
        request,
        'questions/question_create.html',
        {
            'question_form': question_form,
            'choice_formset': choice_formset,
        })


class CreateQuestionView(FormView):
    form_class = AddChoiceForm
    template_name = 'questions/question_create.html'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assessment_id'] = self.kwargs['pk']
        return context


class QuestionDetailView(DetailView):
    model = Question

