from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from candidates.models import CandidateProfile
from assessments.models import Assessment

def recent_activities(request):
    if not request.user.is_hr:
        return HttpResponseForbidden()
    
    activities = [
        {'type': 'System', 'description': 'New assessment created', 'timestamp': timezone.now()}
    ]
    return render(request, 'hr/partials/activity_feed.html', {'activities': activities})

def hr_login(request):
    if request.user.is_authenticated and request.user.is_hr:
        return redirect('hr_dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_hr:
            login(request, user)
            return redirect('hr_dashboard')
        else:
            messages.error(request, 'Invalid credentials or unauthorized access')
    
    return render(request, 'hr/login.html')

@login_required
def hr_dashboard(request):
    if not request.user.is_hr:
        return HttpResponseForbidden("You don't have permission to access this page")
    
    try:
        # Demo activity data - replace with database queries later
        recent_activities = [
            {
                'type': 'Assessment Created',
                'description': 'Frontend Developer Test',
                'timestamp': timezone.now() - timedelta(minutes=15)
            },
            {
                'type': 'Candidate Completed',
                'description': 'John Doe finished Backend Assessment',
                'timestamp': timezone.now() - timedelta(hours=2)
            }
        ]
        
        context = {
            'user': request.user,
            'hr_profile': request.user.hr_profile if hasattr(request.user, 'hr_profile') else None,
            'recent_activities': recent_activities,
            'candidates_count': CandidateProfile.objects.count(),
            'completed_assessments': Assessment.objects.filter(is_completed=True).count()
        }
        
        return render(request, 'hr/dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return HttpResponseServerError("Could not load dashboard")

@login_required
def create_assessment(request):
    if not request.user.is_hr:
        return HttpResponseForbidden("Access denied")
    return render(request, 'hr/create_assessment.html')

@login_required
def view_candidates(request):
    if not request.user.is_hr:
        return HttpResponseForbidden("Access denied")
    return render(request, 'hr/view_candidates.html')

@login_required
def view_results(request):
    if not request.user.is_hr:
        return HttpResponseForbidden("Access denied")
    return render(request, 'hr/view_results.html')

def hr_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out')
    return redirect('hr_login')