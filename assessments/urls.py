from django.urls import include, path

from . import views

app_name = 'assessments'

urlpatterns = [
    path('', views.AssessmentListView.as_view(), name='home'),
    path('create', views.CreateAssessmentView.as_view(), name='create'),
    path('<uuid:pk>', views.AssessmentDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit', views.EditAssessmentView.as_view(), name='edit'),
    path('<uuid:pk>/toggle', views.ToggleAssessmentVisibilityView.as_view(), name='toggle-publish'),
    path('<uuid:pk>/toggle', views.ToggleAssessmentDeleteView.as_view(),
         name='toggle-delete'),
    path('<uuid:assessment_id>/questions/', include('questions.urls', namespace='questions')),

]
