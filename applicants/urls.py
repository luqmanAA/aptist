from django.urls import include, path

from . import views

app_name = 'applicants'

urlpatterns = [
    path('', views.CreateApplicantView.as_view(), name='applicant-signup'),
    # path('assessment/<uuid:pk>', views.take_test_view, name='take-test'),
    path('assessment/<uuid:pk>/tips', views.AssessmentTipView.as_view(), name='test-tip'),
    path('assessment/<uuid:pk>', views.StartAssessmentView.as_view(), name='start-test'),
    path('assessment/<uuid:pk>/completed', views.AssessmentCompleteView.as_view(), name='assessment-completed'),
]
