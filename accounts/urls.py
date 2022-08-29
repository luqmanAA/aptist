from django.urls import include, path

from . import views

app_name = 'accounts'

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    # path('register', views.CreateOrganizationView.as_view(), name='signup'),
    path('profile/', views.redirect_profile_view, name='profile'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('register/organization', views.CreateOrganizationView.as_view(), name='signup'),
    path('register/applicant', include('applicants.urls')),
    path('organization/<slug:slug>', views.OrganizationDetailView.as_view(), name='organization'),
    path('organization/edit/<slug:slug>', views.UpdateOrganizationView.as_view(), name='edit-organization'),
]
