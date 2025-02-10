from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from hr.views import (
    hr_login, hr_dashboard, hr_logout,
    create_assessment, view_candidates, view_results
)
from candidates.views import candidate_login, candidate_dashboard, candidate_logout
from assessments.views import create_assessment, add_questions
from hr.views import recent_activities  # Add this import

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    path('hr/activities/', recent_activities, name='recent_activities'),
    
    # HR authentication routes
    path('hr/login/', hr_login, name='hr_login'),
    path('hr/dashboard/', hr_dashboard, name='hr_dashboard'),
    path('hr/logout/', hr_logout, name='hr_logout'),
    
    # HR functional routes
    path('hr/assessments/create/', create_assessment, name='create_assessment'),
    path('hr/candidates/', view_candidates, name='view_candidates'),
    path('hr/results/', view_results, name='view_results'),
    
    # Candidate routes
    path('candidate/login/', candidate_login, name='candidate_login'),
    path('candidate/dashboard/', candidate_dashboard, name='candidate_dashboard'),
    path('candidate/logout/', candidate_logout, name='candidate_logout'),
    
    # Assessment URLs
    path('hr/assessments/create/', create_assessment, name='create_assessment'),
    path('hr/assessments/<int:assessment_id>/questions/', add_questions, name='add_questions'),

    # Root redirect
    path('', lambda request: redirect('hr_login')),
]