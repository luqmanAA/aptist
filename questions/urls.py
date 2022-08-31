from django.urls import path

from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='list'),
    # path('create', views.CreateQuestionView.as_view(), name='create'),
    path('create', views.create_question_with_choices, name='create'),
    path('<int:pk>', views.QuestionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.EditQuestionView.as_view(), name='edit'),
]
